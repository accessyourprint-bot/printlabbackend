"""
Alt Print - System Configuration Endpoints
Super Admin controls: app state, maintenance, emergency lock
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.db.database import get_db
from app.models.models import SystemConfig, User
from app.schemas.schemas import APIResponse, SystemConfigOut, UpdateAppStateRequest
from app.services.audit import log_action
from app.services.cache import invalidate_system_config_cache
from app.services.websocket import broadcast_system_config_update

router = APIRouter(prefix="/system", tags=["System Config"])


async def _get_config(db: AsyncSession) -> SystemConfig:
    result = await db.execute(select(SystemConfig).where(SystemConfig.id == 1))
    config = result.scalar_one_or_none()
    if not config:
        config = SystemConfig(id=1)
        db.add(config)
        await db.flush()
        await db.refresh(config)
    return config


@router.get("/config", response_model=SystemConfigOut)
async def get_system_config(db: AsyncSession = Depends(get_db)):
    """Get current system configuration (public endpoint - used by all apps)"""
    config = await _get_config(db)
    return config


@router.put("/config", response_model=APIResponse)
async def update_system_config(
    body: UpdateAppStateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Update system configuration (Super Admin only)"""
    config = await _get_config(db)

    changed_fields = {}
    for field, value in body.model_dump(exclude_none=True).items():
        if hasattr(config, field) and getattr(config, field) != value:
            setattr(config, field, value)
            changed_fields[field] = value

    if not changed_fields:
        return APIResponse(message="No changes detected")

    config.updated_by = str(current_user.email or current_user.phone)
    await db.flush()
    await db.refresh(config)

    # Invalidate cache
    await invalidate_system_config_cache()

    # Build config dict for broadcast
    config_dict = {
        "app_enabled": config.app_enabled,
        "maintenance_mode": config.maintenance_mode,
        "emergency_lock": config.emergency_lock,
        "uploads_enabled": config.uploads_enabled,
        "payments_enabled": config.payments_enabled,
        "delivery_enabled": config.delivery_enabled,
        "printing_enabled": config.printing_enabled,
        "login_enabled": config.login_enabled,
        "orders_enabled": config.orders_enabled,
        "changed_fields": changed_fields,
    }

    # Broadcast via WebSocket
    await broadcast_system_config_update(config_dict)

    # Audit log
    await log_action(
        db,
        actor=str(current_user.email or current_user.phone),
        action="UPDATE_APP_STATE",
        target="system",
        details=changed_fields,
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(message="System configuration updated", data=config_dict)


@router.put("/app", response_model=APIResponse)
async def toggle_app(
    request: Request,
    enabled: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Toggle app enabled/disabled"""
    return await update_system_config(
        UpdateAppStateRequest(app_enabled=enabled), request, db, current_user
    )


@router.put("/maintenance", response_model=APIResponse)
async def toggle_maintenance(
    request: Request,
    enabled: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Toggle maintenance mode"""
    return await update_system_config(
        UpdateAppStateRequest(maintenance_mode=enabled), request, db, current_user
    )


@router.put("/emergency", response_model=APIResponse)
async def toggle_emergency_lock(
    request: Request,
    locked: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Toggle emergency lock - immediately halts all transactions"""
    return await update_system_config(
        UpdateAppStateRequest(emergency_lock=locked), request, db, current_user
    )
