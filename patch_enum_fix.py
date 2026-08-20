path = "app/models/models.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

def fail(label, count):
    raise SystemExit(f"FAILED: [{label}] matched {count} times, expected different count.")

old = '''        Enum(
            "pending", "confirmed", "processing",
            "ready", "out_for_delivery", "delivered",
            "cancelled", "refunded",
            name="order_status"
        ),'''

new = '''        Enum(
            "pending", "confirmed", "processing",
            "ready", "accepted", "en_route_pickup", "reached_pickup",
            "out_for_delivery", "delivered",
            "cancelled", "refunded",
            name="order_status"
        ),'''

if src.count(old) != 1:
    fail("order_status enum block", src.count(old))
src = src.replace(old, new, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: order_status enum updated in models.py.")
