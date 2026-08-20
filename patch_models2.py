path = r"app\models\models.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

old = '''    driving_licence_url = Column(String(500), nullable=True)
    vehicle_rc_url = Column(String(500), nullable=True)
    orders_completed = Column(Integer, nullable=False, default=0)'''

new = '''    driving_licence_url = Column(String(500), nullable=True)
    driving_licence_nonce = Column(String(100), nullable=True)
    vehicle_rc_url = Column(String(500), nullable=True)
    vehicle_rc_nonce = Column(String(100), nullable=True)
    orders_completed = Column(Integer, nullable=False, default=0)'''

if src.count(old) != 1:
    raise SystemExit(f"FAILED: found {src.count(old)} matches in models.py, expected 1.")

src = src.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: nonce columns added to DeliveryPerson model.")
