import io

path = "app/api/v1/endpoints/orders.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

changes = []

# 1. Add selectinload(Order.user) to all three .options(selectinload(Order.files)) calls in list_orders
old_opt = ".options(selectinload(Order.files))"
new_opt = ".options(selectinload(Order.files), selectinload(Order.user))"
c1 = content.count(old_opt)
print(f"'.options(selectinload(Order.files))' found {c1} time(s)")
content = content.replace(old_opt, new_opt)
changes.append(f"Added user eager-load to {c1} quer(y/ies)")

# 2. Populate customer_name/customer_phone before appending to output
old_loop = """    for o in orders:
        try:
            out.append(OrderOut.model_validate(o))
        except Exception as e:
            import traceback
            print(f"ORDER VALIDATION ERROR for {o.id}: {e}")
            traceback.print_exc()
    return out"""

new_loop = """    for o in orders:
        try:
            item = OrderOut.model_validate(o)
            if o.user:
                item.customer_name = o.user.full_name or o.user.email or None
                item.customer_phone = o.user.phone or None
            out.append(item)
        except Exception as e:
            import traceback
            print(f"ORDER VALIDATION ERROR for {o.id}: {e}")
            traceback.print_exc()
    return out"""

c2 = content.count(old_loop)
print(f"Return loop anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_loop, new_loop)
    changes.append("Customer name/phone populated in response loop")
else:
    changes.append("WARNING: return loop anchor not unique - manual fix needed")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("\\n".join(changes))
