path = "app/api/v1/endpoints/orders.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

def fail(label, count):
    raise SystemExit(f"FAILED: [{label}] matched {count} times, expected different count.")

# Fix accept: already does a separate select with only Order.user - add Order.files
old1 = 'result = await db.execute(select(Order).options(selectinload(Order.user)).where(Order.id == order_id))\n    order = result.scalar_one()\n    await broadcast_order_update(str(order.id), order.status, str(order.user_id))\n    return OrderOut.model_validate(order)\n\n\n@router.post("/{order_id}/start-ride"'
new1 = 'result = await db.execute(select(Order).options(selectinload(Order.user), selectinload(Order.files)).where(Order.id == order_id))\n    order = result.scalar_one()\n    await broadcast_order_update(str(order.id), order.status, str(order.user_id))\n    return OrderOut.model_validate(order)\n\n\n@router.post("/{order_id}/start-ride"'
if src.count(old1) != 1:
    fail("accept fix", src.count(old1))
src = src.replace(old1, new1, 1)

# Fix _get_order_for_rider helper to eager-load files+user, used by start-ride/reach-pickup/confirm-pickup
old2 = '''async def _get_order_for_rider(db: AsyncSession, order_id: UUID, rider: DeliveryPerson) -> Order:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.delivery_person_id != rider.id:
        raise HTTPException(status_code=403, detail="This order is not assigned to you")
    return order'''

new2 = '''async def _get_order_for_rider(db: AsyncSession, order_id: UUID, rider: DeliveryPerson) -> Order:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.user), selectinload(Order.files))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.delivery_person_id != rider.id:
        raise HTTPException(status_code=403, detail="This order is not assigned to you")
    return order'''

if src.count(old2) != 1:
    fail("_get_order_for_rider fix", src.count(old2))
src = src.replace(old2, new2, 1)

# Fix complete endpoint: with_for_update select needs eager loading too
old3 = '''    result = await db.execute(
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
        return OrderOut.model_validate(order)'''

new3 = '''    result = await db.execute(
        select(Order).where(Order.id == order_id).with_for_update()
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.delivery_person_id != rider.id:
        raise HTTPException(status_code=403, detail="This order is not assigned to you")

    if order.payout_recorded:
        # Already completed - return current state unchanged, no error, no double-count
        reload_result = await db.execute(
            select(Order)
            .options(selectinload(Order.user), selectinload(Order.files))
            .where(Order.id == order_id)
        )
        return OrderOut.model_validate(reload_result.scalar_one())'''

if src.count(old3) != 1:
    fail("complete idempotent-return fix", src.count(old3))
src = src.replace(old3, new3, 1)

# Fix complete endpoint: final return also needs eager loading (currently does db.refresh which lazy-loads)
old4 = '''    await db.flush()
    await db.refresh(order)
    await broadcast_order_update(str(order.id), order.status, str(order.user_id))
    return OrderOut.model_validate(order)
'''
# This pattern appears 4 times (start-ride, reach-pickup, confirm-pickup, complete) - but order comes from
# _get_order_for_rider (already fixed above) for the first 3. Only complete's order came from a bare select.
# Since _get_order_for_rider now eager-loads, db.refresh() after a flush should still work IF the loader
# strategy sticks on refresh. To be safe, explicitly re-select with eager loads on all 4 occurrences.

new4 = '''    await db.flush()
    reload_result = await db.execute(
        select(Order)
        .options(selectinload(Order.user), selectinload(Order.files))
        .where(Order.id == order.id)
    )
    order = reload_result.scalar_one()
    await broadcast_order_update(str(order.id), order.status, str(order.user_id))
    return OrderOut.model_validate(order)
'''

count4 = src.count(old4)
if count4 == 0:
    fail("refresh-pattern fix (none found)", 0)
src = src.replace(old4, new4)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print(f"SUCCESS: eager-loading fixed in accept, _get_order_for_rider, and {count4} refresh-pattern occurrence(s).")
