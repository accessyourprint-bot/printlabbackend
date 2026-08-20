path = "app/schemas/schemas.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

def fail(label, count):
    raise SystemExit(f"FAILED: [{label}] matched {count} times, expected different count.")

old = '''class OrderOut(BaseModel):
    id: UUID
    order_number: str
    shop_id: str
    status: str
    delivery_type: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    printing_cost: float
    color_cost: float
    binding_cost: float
    delivery_cost: float
    subtotal: float
    gst_amount: float
    grand_total: float'''

new = '''class OrderOut(BaseModel):
    id: UUID
    order_number: str
    shop_id: str
    status: str
    delivery_type: str
    delivery_person_id: Optional[UUID] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_lat: Optional[float] = None
    delivery_lng: Optional[float] = None
    printing_cost: float
    color_cost: float
    binding_cost: float
    delivery_cost: float
    subtotal: float
    gst_amount: float
    grand_total: float
    accepted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    reached_pickup_at: Optional[datetime] = None
    picked_up_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    payout_amount: Optional[float] = None'''

if src.count(old) != 1:
    fail("OrderOut block", src.count(old))
src = src.replace(old, new, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: OrderOut schema updated.")
