import io
path = "app/api/v1/endpoints/delivery.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()
print(repr(content[:600]))
