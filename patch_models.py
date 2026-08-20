path = r"app\models\models.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

old = '''    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    location_updated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PrintPricing(Base):'''

new = '''    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    location_updated_at = Column(DateTime(timezone=True), nullable=True)
    city = Column(String(255), nullable=True)
    driving_licence_url = Column(String(500), nullable=True)
    vehicle_rc_url = Column(String(500), nullable=True)
    orders_completed = Column(Integer, nullable=False, default=0)
    total_earned = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PrintPricing(Base):'''

if src.count(old) != 1:
    raise SystemExit(f"FAILED: found {src.count(old)} matches in models.py, expected 1.")

src = src.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: DeliveryPerson model extended.")
