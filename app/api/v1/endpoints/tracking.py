"""
Alt Print - Live Delivery Tracking
Delivery partner location updates + customer-facing tracking fetch
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_client_ip, get_current_user
from app.db.database import get_db
from app.models.models import Order, DeliveryPerson, User
from app.schemas.schemas import APIResponse

router = APIRouter(prefix="/tracking", tags=["Live Tracking"])


class LocationUpdateRequest(BaseModel):
    latitude: float
    longitude: float


class DeliveryLocationOut(BaseModel):
    delivery_person_name: Optional[str] = None
    delivery_person_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    updated_at: Optional[str] = None
    order_status: str
    destination_lat: Optional[float] = None
    destination_lng: Optional[float] = None


class AssignDeliveryRequest(BaseModel):
    delivery_person_id: UUID


@router.post("/delivery-persons/{person_id}/location", response_model=APIResponse)
async def update_delivery_location(
    person_id: UUID,
    body: LocationUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delivery partner app calls this every ~10-15s while on a delivery."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")

    from datetime import datetime, timezone
    person.current_lat = body.latitude
    person.current_lng = body.longitude
    person.location_updated_at = datetime.now(timezone.utc)

    await db.flush()
    return APIResponse(message="Location updated")


@router.get("/orders/{order_id}", response_model=DeliveryLocationOut)
async def get_order_tracking(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Customer app polls this to show the live map."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id and current_user.role not in ("super_admin", "shop_admin"):
        raise HTTPException(status_code=403, detail="Not authorized to view this order")

    person = None
    if order.delivery_person_id:
        p_result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == order.delivery_person_id))
        person = p_result.scalar_one_or_none()

    return DeliveryLocationOut(
        delivery_person_name=person.name if person else None,
        delivery_person_phone=person.phone if person else None,
        latitude=person.current_lat if person else None,
        longitude=person.current_lng if person else None,
        updated_at=person.location_updated_at.isoformat() if person and person.location_updated_at else None,
        order_status=order.status,
        destination_lat=order.delivery_lat,
        destination_lng=order.delivery_lng,
    )


@router.patch("/orders/{order_id}/assign", response_model=APIResponse)
async def assign_delivery_person(
    order_id: UUID,
    body: AssignDeliveryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Admin/shop staff assigns a delivery person to an order."""
    if current_user.role not in ("super_admin", "shop_admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    p_result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == body.delivery_person_id))
    person = p_result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")

    order.delivery_person_id = person.id
    order.status = "out_for_delivery"
    await db.flush()

    return APIResponse(message=f"Assigned {person.name} to order {order.order_number}")
