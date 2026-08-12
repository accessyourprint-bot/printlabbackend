import io

# 1. Add lat/lng/updated_at fields to DeliveryPerson model
path1 = "app/models/models.py"
with io.open(path1, "r", encoding="utf-8") as f:
    content = f.read()

anchor1 = """    current_status = Column(String(20), nullable=False, default="available")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PrintPricing(Base):"""

new1 = """    current_status = Column(String(20), nullable=False, default="available")
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    location_updated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PrintPricing(Base):"""

c1 = content.count(anchor1)
print(f"DeliveryPerson anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(anchor1, new1)
    with io.open(path1, "w", encoding="utf-8") as f:
        f.write(content)
    print("DeliveryPerson model updated")
else:
    print("WARNING: anchor not unique, model NOT updated - manual fix needed")
