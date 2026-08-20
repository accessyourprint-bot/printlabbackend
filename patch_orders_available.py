path = "app/api/v1/endpoints/orders.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

anchor = "@router.post(\"/{order_id}/accept\", response_model=OrderOut)"

if content.count(anchor) != 1:
    print(f"FAIL: expected exactly 1 occurrence of accept-route anchor, found {content.count(anchor)} - aborting.")
    raise SystemExit(1)

new_code = """import math as _math_rider
from app.schemas.schemas import RiderOrderOut


def _distance_and_eta(shop_lat, shop_lng, dest_lat, dest_lng, stored_km):
    \"\"\"Haversine straight-line distance + rough city-speed ETA.
    Prefers a stored/customer-provided distance if present.\"\"\"
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
    \"\"\"Rider app polls this for unassigned, ready home_delivery orders.\"\"\"
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


""" + anchor

content = content.replace(anchor, new_code, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("SUCCESS: GET /orders/available added to orders.py")
