"""
Alt Print - Orders Endpoints
Create orders, calculate pricing, manage order lifecycle
"""
import random
import string
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import datetime, timezone

from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.db.database import get_db
from app.models.models import DeliveryPerson, Order, OrderFile, Shop, SystemConfig, User
from app.schemas.schemas import (
    APIResponse,
    CreateOrderRequest,
    OrderOut,
    PriceBreakdown,
    PriceCalculationRequest,
)
from app.services.pricing import (
    calculate_delivery_cost,
    calculate_file_cost,
    calculate_order_total,
)
from app.services.websocket import broadcast_order_update

router = APIRouter(prefix="/orders", tags=["Orders"])


def _generate_order_number() -> str:
    """Generate a human-readable order number like AP-2024-ABCD1234"""
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"AP-{suffix}"


async def _check_orders_enabled(db: AsyncSession) -> None:
    result = await db.execute(select(SystemConfig).where(SystemConfig.id == 1))
    config = result.scalar_one_or_none()
    if config and (not config.orders_enabled or config.emergency_lock or not config.app_enabled):
        raise HTTPException(status_code=503, detail="Order creation is currently disabled")


@router.post("/calculate-price", response_model=PriceBreakdown)
async def calculate_price(
    body: PriceCalculationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Calculate order price before placing. No order is created."""
    shop_result = await db.execute(
        select(Shop).where(Shop.id == body.shop_id, Shop.is_active == True)
    )
    shop = shop_result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or inactive")
    if (
        body.delivery_type == "home_delivery"
        and body.delivery_distance_km is not None
        and body.delivery_distance_km > shop.delivery_radius_km
    ):
        raise HTTPException(status_code=400, detail="Delivery address is outside the shop radius")

    file_breakdowns = []
    for f in body.files:
        breakdown = calculate_file_cost(
            page_count=f.get("page_count", 1),
            print_color=f.get("print_color", "black_white"),
            copies=f.get("copies", 1),
            is_front_back=f.get("is_front_back", False),
            spiral_binding=f.get("spiral_binding", False),
            colored_binding_sheet=f.get("colored_binding_sheet", False),
        )
        breakdown["file_id"] = f.get("file_id")
        file_breakdowns.append(breakdown)

    delivery_cost = calculate_delivery_cost(
        delivery_type=body.delivery_type,
        distance_km=body.delivery_distance_km,
    )
    totals = calculate_order_total(file_breakdowns, delivery_cost)
    return PriceBreakdown(**totals)


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    body: CreateOrderRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Place a new order.
    Files must be pre-uploaded. Each file can have independent customization.
    """
    await _check_orders_enabled(db)

    # Validate shop
    shop_result = await db.execute(select(Shop).where(Shop.id == body.shop_id, Shop.is_active == True))
    shop = shop_result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or inactive")
    if (
        body.delivery_type == "home_delivery"
        and body.delivery_distance_km is not None
        and body.delivery_distance_km > shop.delivery_radius_km
    ):
        raise HTTPException(status_code=400, detail="Delivery address is outside the shop radius")

    # Validate and fetch files
    if not body.file_ids:
        raise HTTPException(status_code=400, detail="At least one file required")

    files = []
    for fid in body.file_ids:
        result = await db.execute(
            select(OrderFile).where(
                OrderFile.id == fid,
                OrderFile.user_id == current_user.id,
                OrderFile.order_id == None,
                OrderFile.status == "uploaded",
            )
        )
        f = result.scalar_one_or_none()
        if not f:
            raise HTTPException(status_code=400, detail=f"File {fid} not found or already in an order")
        files.append(f)

    # Apply customizations
    file_breakdowns = []
    for f in files:
        custom = body.file_customizations.get(str(f.id))
        if custom:
            f.print_color = custom.print_color
            f.copies = custom.copies
            f.is_front_back = custom.is_front_back
            f.spiral_binding = custom.spiral_binding
            f.colored_binding_sheet = custom.colored_binding_sheet
            f.custom_instructions = custom.custom_instructions

        breakdown = calculate_file_cost(
            page_count=f.page_count,
            print_color=f.print_color,
            copies=f.copies,
            is_front_back=f.is_front_back,
            spiral_binding=f.spiral_binding,
            colored_binding_sheet=f.colored_binding_sheet,
        )
        f.file_cost = breakdown["file_total"]
        file_breakdowns.append(breakdown)

    # Calculate delivery
    delivery_cost = calculate_delivery_cost(
        delivery_type=body.delivery_type,
        distance_km=body.delivery_distance_km,
    )

    totals = calculate_order_total(file_breakdowns, delivery_cost)

    # Create order
    order = Order(
        order_number=_generate_order_number(),
        user_id=current_user.id,
        shop_id=body.shop_id,
        delivery_type=body.delivery_type,
        delivery_address=body.delivery_address,
        delivery_lat=body.delivery_lat,
        delivery_lng=body.delivery_lng,
        delivery_distance_km=body.delivery_distance_km,
        special_instructions=body.special_instructions,
        printing_cost=totals["printing_cost"],
        color_cost=totals["color_cost"],
        binding_cost=totals["binding_cost"],
        delivery_cost=totals["delivery_cost"],
        subtotal=totals["subtotal"],
        gst_amount=totals["gst_amount"],
        grand_total=totals["grand_total"],
        status="pending",
    )
    db.add(order)
    await db.flush()

    # Link files to order
    for f in files:
        f.order_id = order.id
        f.status = "processing"

    await db.flush()
    await db.refresh(order)

    return APIResponse(
        message="Order placed successfully",
        data={
            "order_id": str(order.id),
            "order_number": order.order_number,
            "grand_total": float(order.grand_total),
            "status": order.status,
        },
    )


async def _create_preset_order(body: CreateOrderRequest, request: Request, db: AsyncSession, current_user: User, print_color: str, extra_note: str | None = None):
    body_data = body.model_dump()
    file_customizations = {}
    for file_id in body.file_ids:
        customization = body.file_customizations.get(str(file_id)) or {}
        if isinstance(customization, dict):
            customization["print_color"] = print_color
            file_customizations[str(file_id)] = customization
        else:
            file_customization = customization.model_copy(update={"print_color": print_color})
            file_customizations[str(file_id)] = file_customization

    if extra_note:
        body_data["special_instructions"] = " | ".join(filter(None, [body.special_instructions, extra_note]))

    preset_body = CreateOrderRequest(
        **{**body_data, "file_customizations": file_customizations}
    )
    return await create_order(preset_body, request, db, current_user)


@router.post("/bw-print", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def bw_print(
    body: CreateOrderRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _create_preset_order(body, request, db, current_user, "black_white", "product=bw_print")


@router.post("/colour-print", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def colour_print(
    body: CreateOrderRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _create_preset_order(body, request, db, current_user, "color", "product=colour_print")


@router.post("/photo-print", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def photo_print(
    body: CreateOrderRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _create_preset_order(body, request, db, current_user, "color", "product=photo_print")


@router.post("/tshirt-print", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def tshirt_print(
    body: CreateOrderRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _create_preset_order(body, request, db, current_user, "color", "product=tshirt_print")


@router.get("", response_model=List[OrderOut])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List orders. Users see their own; shop admins see their shop's orders."""
    if current_user.role == "super_admin":
        query = select(Order).options(selectinload(Order.files), selectinload(Order.user)).order_by(Order.created_at.desc())
    elif current_user.role == "shop_admin":
        query = (
            select(Order)
            .options(selectinload(Order.files), selectinload(Order.user))
            .where(Order.shop_id == current_user.shop_id)
            .order_by(Order.created_at.desc())
        )
    elif current_user.role == "rider":
        rider_result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == current_user.id))
        rider = rider_result.scalar_one_or_none()
        if not rider:
            return []
        query = (
            select(Order)
            .options(selectinload(Order.files), selectinload(Order.user))
            .where(Order.delivery_person_id == rider.id)
            .order_by(Order.created_at.desc())
        )
    else:
        query = (
            select(Order)
            .options(selectinload(Order.files), selectinload(Order.user))
            .where(Order.user_id == current_user.id)
            .order_by(Order.created_at.desc())
        )

    result = await db.execute(query)
    orders = result.scalars().all()
    out = []
    for o in orders:
        try:
            item = OrderOut.model_validate(o)
            if o.user:
                item.customer_name = o.user.full_name or o.user.email or None
                item.customer_phone = o.user.phone or None
            out.append(item)
        except Exception as e:
            import traceback
            print(f"ORDER VALIDATION ERROR for {o.id}: {e}")
            traceback.print_exc()
    return out


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific order with all file details"""
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.files), selectinload(Order.user))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Authorization
    if current_user.role == "user" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "shop_admin" and order.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "rider":
        rider_result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == current_user.id))
        rider = rider_result.scalar_one_or_none()
        if not rider or order.delivery_person_id != rider.id:
            raise HTTPException(status_code=403, detail="Access denied")

    return OrderOut.model_validate(order)


@router.patch("/{order_id}/status", response_model=APIResponse)
async def update_order_status(
    order_id: UUID,
    new_status: str,
    request: Request,
    delivery_person_id: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Update order status (shop admin or super admin)"""
    valid_statuses = {"confirmed", "processing", "ready", "out_for_delivery", "delivered", "cancelled"}
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid: {valid_statuses}")

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role == "shop_admin" and order.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")

    order.status = new_status
    if new_status == "out_for_delivery" and delivery_person_id:
        order.delivery_person_id = delivery_person_id
    await db.flush()

    # Broadcast real-time update to the user
    await broadcast_order_update(str(order.id), new_status, str(order.user_id))

    return APIResponse(message=f"Order status updated to {new_status}")


async def _get_rider_or_403(db: AsyncSession, current_user: User) -> DeliveryPerson:
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == current_user.id))
    rider = result.scalar_one_or_none()
    if not rider:
        raise HTTPException(status_code=403, detail="No rider profile linked to this account")
    return rider


async def _get_order_for_rider(db: AsyncSession, order_id: UUID, rider: DeliveryPerson) -> Order:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.delivery_person_id != rider.id:
        raise HTTPException(status_code=403, detail="This order is not assigned to you")
    return order


import math as _math_rider
from app.schemas.schemas import RiderOrderOut


def _distance_and_eta(shop_lat, shop_lng, dest_lat, dest_lng, stored_km):
    """Haversine straight-line distance + rough city-speed ETA.
    Prefers a stored/customer-provided distance if present."""
    if stored_km is not None:
        distance_km = float(stored_km)
        estimated = False
    elif None not in (shop_lat, shop_lng, dest_lat, dest_lng):
        R = 6371.0
        phi1, phi2 = _math_rider.radians(shop_lat), _math_rider.radians(dest_lat)
        dphi = _math_rider.radians(dest_lat - shop_lat)
        dlambda = _math_rider.radians(dest_lng - shop_lng)
        a = (_math_rider.sin(dphi / 2) ** 2
             + _math_rider.cos(phi1) * _math_rider.cos(phi2) * _math_rider.sin(dlambda / 2) ** 2)
        distance_km = round(R * 2 * _math_rider.atan2(_math_rider.sqrt(a), _math_rider.sqrt(1 - a)), 1)
        estimated = True
    else:
        return None, None, False
    eta_min = max(3, round((distance_km / 20.0) * 60))
    return distance_km, eta_min, estimated


@router.get("/available", response_model=List[RiderOrderOut])
async def list_available_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("rider")),
):
    """Rider app polls this for unassigned, ready home_delivery orders."""
    rider = await _get_rider_or_403(db, current_user)
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.shop))
        .where(
            Order.status == "ready",
            Order.delivery_person_id.is_(None),
            Order.delivery_type == "home_delivery",
            Order.shop_id == rider.shop_id,
        )
        .order_by(Order.created_at.asc())
    )
    orders = result.scalars().all()

    out = []
    for order in orders:
        shop = order.shop
        distance_km, eta_min, estimated = _distance_and_eta(
            getattr(shop, "latitude", None),
            getattr(shop, "longitude", None),
            order.delivery_lat,
            order.delivery_lng,
            order.delivery_distance_km,
        )
        item = RiderOrderOut.model_validate(order)
        item.shop_name = getattr(shop, "name", None)
        item.shop_address = getattr(shop, "address", None)
        item.distance_km = distance_km
        item.eta_min = eta_min
        item.distance_estimated = estimated
        out.append(item)
    return out


@router.post("/{order_id}/accept", response_model=OrderOut)
async def rider_accept_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("rider")),
):
    """Rider accepts an order. Atomic — prevents two riders claiming the same order."""
    rider = await _get_rider_or_403(db, current_user)

    now = datetime.now(timezone.utc)
    stmt = (
        sa_update(Order)
        .where(Order.id == order_id, Order.status == "ready", Order.delivery_person_id.is_(None))
        .values(status="accepted", delivery_person_id=rider.id, accepted_at=now)
        .returning(Order.id)
    )
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        # Figure out why, to give a useful error
        check = await db.execute(select(Order).where(Order.id == order_id))
        existing = check.scalar_one_or_none()
        if not existing:
            raise HTTPException(status_code=404, detail="Order not found")
        if existing.delivery_person_id is not None:
            raise HTTPException(status_code=409, detail="Order already accepted by another rider")
        raise HTTPException(status_code=409, detail=f"Order is not available to accept (status: {existing.status})")

    await db.flush()
    result = await db.execute(select(Order).options(selectinload(Order.user)).where(Order.id == order_id))
    order = result.scalar_one()
    await broadcast_order_update(str(order.id), order.status, str(order.user_id))
    return OrderOut.model_validate(order)


@router.post("/{order_id}/start-ride", response_model=OrderOut)
async def rider_start_ride(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("rider")),
):
    rider = await _get_rider_or_403(db, current_user)
    order = await _get_order_for_rider(db, order_id, rider)
    if order.status != "accepted":
        raise HTTPException(status_code=409, detail=f"Cannot start ride from status: {order.status}")
    order.status = "en_route_pickup"
    order.started_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(order)
    await broadcast_order_update(str(order.id), order.status, str(order.user_id))
    return OrderOut.model_validate(order)


@router.post("/{order_id}/reach-pickup", response_model=OrderOut)
async def rider_reach_pickup(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("rider")),
):
    rider = await _get_rider_or_403(db, current_user)
    order = await _get_order_for_rider(db, order_id, rider)
    if order.status != "en_route_pickup":
        raise HTTPException(status_code=409, detail=f"Cannot reach pickup from status: {order.status}")
    order.status = "reached_pickup"
    order.reached_pickup_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(order)
    await broadcast_order_update(str(order.id), order.status, str(order.user_id))
    return OrderOut.model_validate(order)


@router.post("/{order_id}/confirm-pickup", response_model=OrderOut)
async def rider_confirm_pickup(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("rider")),
):
    rider = await _get_rider_or_403(db, current_user)
    order = await _get_order_for_rider(db, order_id, rider)
    if order.status != "reached_pickup":
        raise HTTPException(status_code=409, detail=f"Cannot confirm pickup from status: {order.status}")
    order.status = "out_for_delivery"
    order.picked_up_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(order)
    await broadcast_order_update(str(order.id), order.status, str(order.user_id))
    return OrderOut.model_validate(order)


@router.post("/{order_id}/complete", response_model=OrderOut)
async def rider_complete_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("rider")),
):
    """Idempotent: safe to double-tap or retry. Payout/earnings applied exactly once."""
    rider = await _get_rider_or_403(db, current_user)

    # Lock the order row to serialize concurrent completion attempts
    result = await db.execute(
        select(Order).where(Order.id == order_id).with_for_update()
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.delivery_person_id != rider.id:
        raise HTTPException(status_code=403, detail="This order is not assigned to you")

    if order.payout_recorded:
        # Already completed - return current state unchanged, no error, no double-count
        await db.refresh(order)
        return OrderOut.model_validate(order)

    if order.status != "out_for_delivery":
        raise HTTPException(status_code=409, detail=f"Cannot complete order from status: {order.status}")

    now = datetime.now(timezone.utc)
    payout = order.delivery_cost or 0

    order.status = "delivered"
    order.completed_at = now
    order.payout_amount = payout
    order.payout_recorded = True

    # Lock the rider row too, then increment
    rider_result = await db.execute(
        select(DeliveryPerson).where(DeliveryPerson.id == rider.id).with_for_update()
    )
    rider_locked = rider_result.scalar_one()
    rider_locked.orders_completed = (rider_locked.orders_completed or 0) + 1
    rider_locked.total_earned = (rider_locked.total_earned or 0) + payout
    rider_locked.current_status = "available"

    await db.flush()
    await db.refresh(order)
    await broadcast_order_update(str(order.id), order.status, str(order.user_id))
    return OrderOut.model_validate(order)
