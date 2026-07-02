import asyncio, sys
sys.path.insert(0, ".")
from app.schemas.schemas import OrderOut
from uuid import UUID
from datetime import datetime

# Simulate what the DB returns
test = {
    "id": "e31129f8-5207-4e5f-a812-8bc45bd77182",
    "order_number": "ORD-A001",
    "shop_id": "shop-001",
    "status": "processing",
    "delivery_type": "self_pickup",
    "printing_cost": 1200.0,
    "color_cost": 0.0,
    "binding_cost": 0.0,
    "delivery_cost": 0.0,
    "subtotal": 1200.0,
    "gst_amount": 0.0,
    "grand_total": 1200.0,
    "files": [],
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}
try:
    o = OrderOut(**test)
    print("OK:", o)
except Exception as e:
    print("ERROR:", e)
