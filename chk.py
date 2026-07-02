import subprocess, json

r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',
    "SELECT id, order_number, status, delivery_type, grand_total, color_cost, binding_cost, delivery_cost, subtotal, gst_amount, updated_at FROM orders LIMIT 3;"],
    capture_output=True, text=True)
print(r.stdout)
