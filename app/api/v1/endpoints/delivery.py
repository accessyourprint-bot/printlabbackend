"""
Alt Print - Delivery Person Management Endpoints
Shop admins manage their own delivery staff; super admin manages all.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import DeliveryPerson, Order, User
from app.schemas.schemas import APIResponse, DeliveryPersonCreate, DeliveryPersonOut, DeliveryPersonUpdate, DeliveryPersonWithCountOut

router = APIRouter(prefix="/delivery-persons", tags=["Delivery"])


@router.get("", response_model=List[DeliveryPersonOut])
async def list_delivery_persons(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """List delivery persons. Shop admins see only their own shop."""
    query = select(DeliveryPerson)
    if current_user.role == "shop_admin":
        query = query.where(DeliveryPerson.shop_id == current_user.shop_id)
    elif shop_id:
        query = query.where(DeliveryPerson.shop_id == shop_id)

    result = await db.execute(query.order_by(DeliveryPerson.name))
    persons = result.scalars().all()
    return [DeliveryPersonOut.model_validate(p) for p in persons]


@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])
async def list_delivery_persons_with_counts(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """List delivery persons along with how many orders each has been assigned."""
    query = select(DeliveryPerson)
    if current_user.role == "shop_admin":
        query = query.where(DeliveryPerson.shop_id == current_user.shop_id)
    elif shop_id:
        query = query.where(DeliveryPerson.shop_id == shop_id)
    result = await db.execute(query.order_by(DeliveryPerson.name))
    persons = result.scalars().all()

    count_result = await db.execute(
        select(Order.delivery_person_id, func.count(Order.id))
        .where(Order.delivery_person_id.isnot(None))
        .group_by(Order.delivery_person_id)
    )
    counts = dict(count_result.all())

    out = []
    for p in persons:
        item = DeliveryPersonWithCountOut.model_validate(p)
        item.order_count = counts.get(p.id, 0)
        out.append(item)
    return out


@router.post("", response_model=APIResponse, status_code=201)
async def create_delivery_person(
    body: DeliveryPersonCreate,
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Add a new delivery person."""
    target_shop_id = current_user.shop_id if current_user.role == "shop_admin" else shop_id
    if not target_shop_id:
        raise HTTPException(status_code=400, detail="shop_id is required")

    person = DeliveryPerson(
        shop_id=target_shop_id,
        name=body.name,
        phone=body.phone,
        vehicle_number=body.vehicle_number,
    )
    db.add(person)
    await db.flush()
    await db.refresh(person)
    return APIResponse(message="Delivery person added", data={"id": str(person.id)})


@router.patch("/{person_id}", response_model=APIResponse)
async def update_delivery_person(
    person_id: str,
    body: DeliveryPersonUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Update a delivery person's details or status."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")

    for field in ("name", "phone", "vehicle_number", "is_active", "current_status"):
        value = getattr(body, field)
        if value is not None:
            setattr(person, field, value)

    await db.flush()
    return APIResponse(message="Delivery person updated", data={"id": person_id})


@router.delete("/{person_id}", response_model=APIResponse)
async def delete_delivery_person(
    person_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Remove a delivery person."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")

    await db.delete(person)
    await db.flush()
    return APIResponse(message="Delivery person removed", data={"id": person_id})
