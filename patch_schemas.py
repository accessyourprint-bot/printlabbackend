path = r"app\schemas\schemas.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

old = """class DeliveryPersonCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., min_length=10, max_length=15)
    vehicle_number: Optional[str] = None


class DeliveryPersonUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    vehicle_number: Optional[str] = None
    is_active: Optional[bool] = None
    current_status: Optional[str] = Field(None, pattern="^(available|busy|offline)$")


class DeliveryPersonOut(BaseModel):
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

new = """class DeliveryPersonCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., min_length=10, max_length=15)
    vehicle_number: Optional[str] = None
    city: Optional[str] = None


class DeliveryPersonUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    vehicle_number: Optional[str] = None
    is_active: Optional[bool] = None
    current_status: Optional[str] = Field(None, pattern="^(available|busy|offline)$")
    city: Optional[str] = None
    driving_licence_url: Optional[str] = None
    vehicle_rc_url: Optional[str] = None


class DeliveryPersonOut(BaseModel):
    id: UUID
    shop_id: str
    name: str
    phone: str
    vehicle_number: Optional[str] = None
    is_active: bool
    current_status: str
    city: Optional[str] = None
    driving_licence_url: Optional[str] = None
    vehicle_rc_url: Optional[str] = None
    orders_completed: int = 0
    total_earned: float = 0
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    location_updated_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True"""

if src.count(old) != 1:
    raise SystemExit(f"FAILED: found {src.count(old)} matches in schemas.py, expected 1.")

src = src.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: DeliveryPerson schemas extended.")
