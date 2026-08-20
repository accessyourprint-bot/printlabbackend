path = r"app\api\v1\endpoints\delivery.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()
old = "from app.api.v1.deps import require_role"
new = "from app.api.v1.deps import require_role, get_current_user"
if src.count(old) != 1:
    raise SystemExit(f"FAILED: found {src.count(old)} matches, expected 1.")
src = src.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("SUCCESS: get_current_user imported.")
