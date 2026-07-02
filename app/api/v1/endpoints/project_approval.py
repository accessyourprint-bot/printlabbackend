"""
Alt Print - Project Approval Endpoints (Super Admin)
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import OrderFile, User
from app.schemas.schemas import APIResponse, OrderFileOut

router = APIRouter(prefix="/admin/projects", tags=["Project Approval"])


@router.get("/pending", response_model=List[OrderFileOut])
async def list_pending_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """List all projects awaiting approval."""
    result = await db.execute(
        select(OrderFile).where(OrderFile.status == "pending_approval").order_by(OrderFile.created_at.asc())
    )
    files = result.scalars().all()
    return [OrderFileOut.model_validate(f) for f in files]


@router.post("/{project_id}/approve", response_model=APIResponse)
async def approve_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Approve a pending project."""
    result = await db.execute(select(OrderFile).where(OrderFile.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.status = "approved"
    await db.flush()
    return APIResponse(message="Project approved", data={"project_id": project_id, "status": "approved"})


@router.post("/{project_id}/reject", response_model=APIResponse)
async def reject_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Reject a pending project."""
    result = await db.execute(select(OrderFile).where(OrderFile.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.status = "rejected"
    await db.flush()
    return APIResponse(message="Project rejected", data={"project_id": project_id, "status": "rejected"})
