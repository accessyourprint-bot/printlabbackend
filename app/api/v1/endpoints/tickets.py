"""
Alt Print - Outlet Help / Support Ticket Endpoints
Shop admins raise tickets; super admin resolves them.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import SupportTicket, User
from app.schemas.schemas import APIResponse, TicketCreate, TicketOut, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", response_model=APIResponse, status_code=201)
async def create_ticket(
    body: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Raise a support ticket for the current shop."""
    if not current_user.shop_id:
        raise HTTPException(status_code=400, detail="User is not linked to a shop")

    ticket = SupportTicket(
        shop_id=current_user.shop_id,
        created_by=current_user.id,
        subject=body.subject,
        description=body.description,
        priority=body.priority,
        image_url=body.image_url,
        raised_by=body.raised_by,
    )
    db.add(ticket)
    await db.flush()
    await db.refresh(ticket)
    return APIResponse(message="Ticket created", data={"id": str(ticket.id)})


@router.get("", response_model=List[TicketOut])
async def list_tickets(
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """List tickets. Shop admins see their own; super admin sees all."""
    query = select(SupportTicket)
    if current_user.role == "shop_admin":
        query = query.where(SupportTicket.shop_id == current_user.shop_id)
    if status_filter:
        query = query.where(SupportTicket.status == status_filter)

    result = await db.execute(query.order_by(SupportTicket.created_at.desc()))
    tickets = result.scalars().all()
    return [TicketOut.model_validate(t) for t in tickets]


@router.patch("/{ticket_id}", response_model=APIResponse)
async def update_ticket(
    ticket_id: str,
    body: TicketUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Update ticket status / admin response (Super Admin only)."""
    result = await db.execute(select(SupportTicket).where(SupportTicket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if body.status is not None:
        ticket.status = body.status
        if body.status in ("resolved", "closed"):
            ticket.resolved_by = current_user.id
    if body.admin_response is not None:
        ticket.admin_response = body.admin_response

    await db.flush()
    return APIResponse(message="Ticket updated", data={"id": ticket_id, "status": ticket.status})
