"""
Alt Print - Audit Log Endpoints
View system audit trail
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import AuditLog, User
from app.schemas.schemas import AuditLogOut, PaginatedResponse

router = APIRouter(prefix="/audit", tags=["Audit Log"])


@router.get("", response_model=PaginatedResponse)
async def get_audit_logs(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    actor: Optional[str] = None,
    action: Optional[str] = None,
    target: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Get audit logs with optional filtering (Super Admin only)"""
    query = select(AuditLog)

    if actor:
        query = query.where(AuditLog.actor.ilike(f"%{actor}%"))
    if action:
        query = query.where(AuditLog.action == action)
    if target:
        query = query.where(AuditLog.target.ilike(f"%{target}%"))

    # Count total
    from sqlalchemy import func, select as sa_select
    count_query = sa_select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Paginate
    offset = (page - 1) * per_page
    query = query.order_by(AuditLog.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    logs = result.scalars().all()

    return PaginatedResponse(
        items=[AuditLogOut.model_validate(log) for log in logs],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
    )
