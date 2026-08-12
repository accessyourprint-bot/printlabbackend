"""
Alt Print - App Appearance Endpoint
Single-row global appearance settings (colors, font, logo, banner)
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.db.database import get_db
from app.models.models import AppAppearance, User
from app.schemas.schemas import AppAppearanceOut, UpdateAppAppearanceRequest, APIResponse
from app.services.audit import log_action

router = APIRouter(prefix="/appearance", tags=["App Appearance"])


@router.get("", response_model=AppAppearanceOut)
async def get_appearance(db: AsyncSession = Depends(get_db)):
    """Get current app appearance settings (public - used by mobile app)"""
    result = await db.execute(select(AppAppearance).where(AppAppearance.id == 1))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Appearance settings not initialized")
    return row


@router.put("", response_model=APIResponse)
async def update_appearance(
    body: UpdateAppAppearanceRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Update app appearance settings"""
    result = await db.execute(select(AppAppearance).where(AppAppearance.id == 1))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Appearance settings not initialized")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(row, key, value)

    await db.flush()
    await db.refresh(row)

    await log_action(
        db,
        actor=str(current_user.email or current_user.phone),
        action="UPDATE_APPEARANCE",
        target="app_appearance",
        details=update_data,
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(message="Appearance updated", data=AppAppearanceOut.model_validate(row))
