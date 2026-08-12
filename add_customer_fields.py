import io

path = "app/schemas/schemas.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """class OrderOut(BaseModel):
    id: UUID
    order_number: str
    shop_id: str
    status: str
    delivery_type: str"""

new = """class OrderOut(BaseModel):
    id: UUID
    order_number: str
    shop_id: str
    status: str
    delivery_type: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None"""

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OrderOut schema updated")
else:
    print("WARNING: anchor not unique")
