path = "app/api/v1/endpoints/orders.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

def fail(label, count):
    raise SystemExit(f"FAILED: [{label}] matched {count} times, expected different count.")

# 1. Update imports: add DeliveryPerson model, datetime, sqlalchemy update
old_imports = """from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.db.database import get_db
from app.models.models import Order, OrderFile, Shop, SystemConfig, User"""

new_imports = """from datetime import datetime, timezone

from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.db.database import get_db
from app.models.models import DeliveryPerson, Order, OrderFile, Shop, SystemConfig, User"""

if src.count(old_imports) != 1:
    fail("imports block", src.count(old_imports))
src = src.replace(old_imports, new_imports, 1)

old_sa_import = "from sqlalchemy import select"
new_sa_import = "from sqlalchemy import select, update as sa_update"
if src.count(old_sa_import) != 1:
    fail("sqlalchemy import", src.count(old_sa_import))
src = src.replace(old_sa_import, new_sa_import, 1)

# 2. Fix list_orders: riders should see orders assigned to them, not orders they "own" as user_id
old_list = '''    else:
        query = (
            select(Order)
            .options(selectinload(Order.files), selectinload(Order.user))
            .where(Order.user_id == current_user.id)
            .order_by(Order.created_at.desc())
        )'''

new_list = '''    elif current_user.role == "rider":
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
        )'''

if src.count(old_list) != 1:
    fail("list_orders branch", src.count(old_list))
src = src.replace(old_list, new_list, 1)

# 3. Fix get_order authorization to allow the assigned rider through
old_auth = '''    # Authorization
    if current_user.role == "user" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "shop_admin" and order.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return OrderOut.model_validate(order)'''

new_auth = '''    # Authorization
    if current_user.role == "user" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "shop_admin" and order.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "rider":
        rider_result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == current_user.id))
        rider = rider_result.scalar_one_or_none()
        if not rider or order.delivery_person_id != rider.id:
            raise HTTPException(status_code=403, detail="Access denied")

    return OrderOut.model_validate(order)'''

if src.count(old_auth) != 1:
    fail("get_order auth block", src.count(old_auth))
src = src.replace(old_auth, new_auth, 1)

# 4. Append rider lifecycle endpoints at end of file
rider_endpoints = '''

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
'''

if "rider_accept_order" in src:
    fail("rider endpoints already present", 1)

src = src.rstrip() + "\n" + rider_endpoints

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: orders.py updated with rider lifecycle endpoints.")
