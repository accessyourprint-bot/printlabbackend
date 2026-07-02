with open("app/api/v1/endpoints/orders.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '''    out = []
    for o in orders:
        try:
            out.append(OrderOut.model_validate(o))
        except Exception:
            pass
    return out'''

new = '''    out = []
    for o in orders:
        try:
            out.append(OrderOut.model_validate(o))
        except Exception as e:
            import traceback
            print(f"ORDER VALIDATION ERROR for {o.id}: {e}")
            traceback.print_exc()
    return out'''

content = content.replace(old, new)
with open("app/api/v1/endpoints/orders.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched")
