import io
path = "app/core/config.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()
old = "LOGIN_RATE_LIMIT_PER_MINUTE: int = 5"
new = "LOGIN_RATE_LIMIT_PER_MINUTE: int = 100"
count = content.count(old)
print(f"Found {count} occurrence(s)")
content = content.replace(old, new)
with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
