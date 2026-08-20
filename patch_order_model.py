path = "app/models/models.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

def fail(label, count):
    raise SystemExit(f"FAILED: [{label}] matched {count} times, expected different count.")

old = """    is_downloaded = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)"""

new = """    is_downloaded = Column(Boolean, default=False, nullable=False)

    # Rider lifecycle timestamps
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    reached_pickup_at = Column(DateTime(timezone=True), nullable=True)
    picked_up_at = Column(DateTime(timezone=True), nullable=True)
    payout_amount = Column(Numeric(10, 2), nullable=True)
    payout_recorded = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)"""

if src.count(old) != 1:
    fail("Order columns block", src.count(old))
src = src.replace(old, new, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: Order model updated with rider lifecycle columns.")
