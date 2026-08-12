import io

# ---- 1. Add DeliveryPersonWithCountOut schema ----
path = "app/schemas/schemas.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """class DeliveryPersonOut(BaseModel):
    id: UUID
    shop_id: str
    name: str
    phone: str
    vehicle_number: Optional[str] = None
    is_active: bool
    current_status: str
    created_at: datetime

    class Config:
        from_attributes = True"""

new = """class DeliveryPersonOut(BaseModel):
    id: UUID
    shop_id: str
    name: str
    phone: str
    vehicle_number: Optional[str] = None
    is_active: bool
    current_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DeliveryPersonWithCountOut(DeliveryPersonOut):
    order_count: int = 0"""

c1 = content.count(old)
print(f"Schema anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old, new)
    print("DeliveryPersonWithCountOut schema added")
else:
    print("WARNING: schema anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
