import io
path = "app/models/models.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()
anchor = "class Order(Base):"
idx = content.find(anchor)
print("Order class found:", idx != -1)
