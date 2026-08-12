import io

path = "app/api/v1/endpoints/orders.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """async def update_order_status(
    order_id: UUID,
    new_status: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    \"\"\"Update order status (shop admin or super admin)\"\"\"
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
    await db.flush()"""

new = """async def update_order_status(
    order_id: UUID,
    new_status: str,
    request: Request,
    delivery_person_id: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    \"\"\"Update order status (shop admin or super admin)\"\"\"
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
    await db.flush()"""

c = content.count(old)
print(f"update_order_status found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("Endpoint now accepts delivery_person_id")
else:
    print("WARNING: block not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
