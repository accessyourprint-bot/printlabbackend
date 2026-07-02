"""
Alt Print - Admin Control Endpoints
Owner-maintenance and user-control APIs for the web admin panels.
"""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.v1.deps import get_client_ip, require_role
from app.db.database import get_db
from app.models.models import Order, Shop, SystemConfig, User
from app.schemas.schemas import APIResponse, AdminOverviewOut, AdminUserOut, ShopOut, SystemConfigOut
from app.services.audit import log_action

router = APIRouter(prefix="/admin", tags=["Admin Control"])


async def _get_config(db: AsyncSession) -> SystemConfig:
    result = await db.execute(select(SystemConfig).where(SystemConfig.id == 1))
    config = result.scalar_one_or_none()
    if not config:
        config = SystemConfig(id=1)
        db.add(config)
        await db.flush()
        await db.refresh(config)
    return config


@router.get("/owner", response_model=AdminOverviewOut)
async def owner_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Owner maintenance dashboard data."""
    config = await _get_config(db)

    user_count = await db.scalar(select(func.count()).select_from(User))
    shop_count = await db.scalar(select(func.count()).select_from(Shop))
    order_count = await db.scalar(select(func.count()).select_from(Order))
    active_users = await db.scalar(select(func.count()).select_from(User).where(User.is_active == True))

    shops_result = await db.execute(select(Shop).order_by(Shop.created_at.desc()))
    shops = [ShopOut.model_validate(shop) for shop in shops_result.scalars().all()]

    return AdminOverviewOut(
        system_config=SystemConfigOut.model_validate(config),
        totals={
            "users": int(user_count or 0),
            "active_users": int(active_users or 0),
            "shops": int(shop_count or 0),
            "orders": int(order_count or 0),
        },
        shops=shops,
    )


@router.get("/users", response_model=list[AdminUserOut])
async def user_control_panel(
    role: str | None = None,
    shop_id: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """List users for specific-control management."""
    query = select(User)
    if role:
        query = query.where(User.role == role)
    if shop_id:
        query = query.where(User.shop_id == shop_id)

    result = await db.execute(query.order_by(User.created_at.desc()))
    return [AdminUserOut.model_validate(user) for user in result.scalars().all()]


@router.patch("/users/{user_id}/status", response_model=APIResponse)
async def toggle_user_status(
    user_id: str,
    enabled: bool,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Enable or disable a specific user."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = enabled
    await db.flush()

    await log_action(
        db,
        actor=str(current_user.email or current_user.phone),
        action="TOGGLE_USER_STATUS",
        target=str(user.id),
        details={"enabled": enabled},
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(message=f"User {'enabled' if enabled else 'disabled'} successfully")


@router.get("/owner/config", response_model=SystemConfigOut)
async def owner_config(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Owner maintenance config snapshot."""
    config = await _get_config(db)
    return config