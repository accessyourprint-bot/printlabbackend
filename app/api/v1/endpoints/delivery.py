"""
Alt Print - Delivery Person Management Endpoints
Shop admins manage their own delivery staff; super admin manages all.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role, get_current_user
from app.db.database import get_db
from app.models.models import DeliveryPerson, Order, User
from app.schemas.schemas import APIResponse, DeliveryPersonCreate, DeliveryPersonOut, DeliveryPersonUpdate, DeliveryPersonWithCountOut
from app.services.storage import upload_encrypted_file, download_decrypted_file

RIDER_DOC_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
RIDER_DOC_MAX_BYTES = 10 * 1024 * 1024  # 10MB

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


@router.get("/me", response_model=DeliveryPersonOut)
async def get_my_rider_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Rider app calls this after login to get its own profile."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == current_user.id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="No rider profile linked to this account")
    return person


@router.get("/{person_id}", response_model=DeliveryPersonOut)
async def get_delivery_person(
    person_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Full profile for a single delivery person (rider details page)."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")
    return person


@router.post("/{person_id}/documents", response_model=DeliveryPersonOut)
async def upload_rider_document(
    person_id: str,
    doc_type: str = Form(..., pattern="^(driving_licence|vehicle_rc)$"),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Upload (or replace) a rider's driving licence or vehicle RC. Stored encrypted."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")

    content_type = file.content_type or ""
    if content_type not in RIDER_DOC_ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WEBP, or PDF allowed")

    file_data = await file.read()
    if len(file_data) == 0:
        raise HTTPException(status_code=400, detail="Empty file not allowed")
    if len(file_data) > RIDER_DOC_MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large. Maximum size: 10MB")

    try:
        storage_key, nonce_hex = await upload_encrypted_file(
            file_data=file_data,
            original_filename=file.filename or doc_type,
            content_type=content_type,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if doc_type == "driving_licence":
        person.driving_licence_url = storage_key
        person.driving_licence_nonce = nonce_hex
    else:
        person.vehicle_rc_url = storage_key
        person.vehicle_rc_nonce = nonce_hex

    await db.commit()
    await db.refresh(person)
    return person


@router.get("/{person_id}/documents/{doc_type}/download")
async def download_rider_document(
    person_id: str,
    doc_type: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Download and decrypt a rider's driving licence or vehicle RC."""
    if doc_type not in ("driving_licence", "vehicle_rc"):
        raise HTTPException(status_code=400, detail="doc_type must be driving_licence or vehicle_rc")

    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")

    storage_key = person.driving_licence_url if doc_type == "driving_licence" else person.vehicle_rc_url
    nonce_hex = person.driving_licence_nonce if doc_type == "driving_licence" else person.vehicle_rc_nonce

    if not storage_key or not nonce_hex:
        raise HTTPException(status_code=404, detail=f"No {doc_type} uploaded for this rider")

    file_bytes = await download_decrypted_file(storage_key, nonce_hex)
    return Response(content=file_bytes, media_type="application/octet-stream")


@router.patch("/{person_id}/link-user", response_model=DeliveryPersonOut)
async def link_delivery_person_to_user(
    person_id: str,
    phone: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Link an existing delivery person to a login-capable user account by phone.
    Finds or creates the User, sets role=rider, and links delivery_persons.user_id."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")

    user_result = await db.execute(select(User).where(User.phone == phone))
    linked_user = user_result.scalar_one_or_none()

    if linked_user:
        if linked_user.role not in ("rider", "user"):
            raise HTTPException(status_code=400, detail=f"Phone already belongs to a {linked_user.role} account")
        linked_user.role = "rider"
    else:
        import uuid as _uuid
        linked_user = User(id=_uuid.uuid4(), phone=phone, role="rider", full_name=person.name, is_active=True, is_verified=True)
        db.add(linked_user)
        await db.flush()

    existing_link = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == linked_user.id))
    if existing_link.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="This phone is already linked to another rider profile")

    person.user_id = linked_user.id
    await db.commit()
    await db.refresh(person)
    return person


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
