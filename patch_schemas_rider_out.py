path = "app/schemas/schemas.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

anchor = """    files: List[OrderFileOut] = []
    is_downloaded: bool = False
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True"""

if anchor not in content:
    print("FAIL: OrderOut anchor not found - aborting, nothing changed.")
    raise SystemExit(1)

rider_schema = """

class RiderOrderOut(BaseModel):
    id: UUID
    order_number: str
    status: str
    delivery_type: str
    grand_total: float
    delivery_cost: float
    shop_name: Optional[str] = None
    shop_address: Optional[str] = None
    delivery_address: Optional[str] = None
    distance_km: Optional[float] = None
    eta_min: Optional[int] = None
    distance_estimated: bool = False
    created_at: datetime

    class Config:
        from_attributes = True"""

content = content.replace(anchor, anchor + rider_schema, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("SUCCESS: RiderOrderOut added to schemas.py")
