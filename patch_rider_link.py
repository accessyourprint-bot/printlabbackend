path = r"app\models\models.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

old_role = '''    role = Column(
        Enum("super_admin", "shop_admin", "user", name="user_role"),
        nullable=False,
        default="user"
    )'''

new_role = '''    role = Column(
        Enum("super_admin", "shop_admin", "user", "rider", name="user_role"),
        nullable=False,
        default="user"
    )'''

if src.count(old_role) != 1:
    raise SystemExit(f"FAILED: found {src.count(old_role)} matches for role enum, expected 1.")
src = src.replace(old_role, new_role, 1)

old_dp = '''    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)'''

new_dp = '''    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, unique=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)'''

if src.count(old_dp) != 1:
    raise SystemExit(f"FAILED: found {src.count(old_dp)} matches for DeliveryPerson start, expected 1.")
src = src.replace(old_dp, new_dp, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: rider role added, DeliveryPerson.user_id link added.")
