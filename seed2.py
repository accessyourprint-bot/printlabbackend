import subprocess

def psql(sql):
    r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c', sql], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',"SELECT id FROM users WHERE email='admin@altprint.in';"], capture_output=True, text=True)
uid = r.stdout.strip()

# Orders - using correct columns
psql(f"""
INSERT INTO orders (id, order_number, user_id, shop_id, status, delivery_type, grand_total, printing_cost, created_at, completed_at)
VALUES
  (gen_random_uuid(), 'ORD-001', '{uid}', 'shop-001', 'printing', 'pickup', 1200.00, 1200.00, NOW()-INTERVAL '2 hours', NULL),
  (gen_random_uuid(), 'ORD-002', '{uid}', 'shop-001', 'confirmed', 'pickup', 3500.00, 3500.00, NOW()-INTERVAL '1 hour', NULL),
  (gen_random_uuid(), 'ORD-003', '{uid}', 'shop-001', 'printing', 'delivery', 4500.00, 4500.00, NOW()-INTERVAL '30 minutes', NULL),
  (gen_random_uuid(), 'ORD-004', '{uid}', 'shop-001', 'completed', 'pickup', 800.00, 800.00, NOW()-INTERVAL '5 hours', NOW()-INTERVAL '1 hour'),
  (gen_random_uuid(), 'ORD-005', '{uid}', 'shop-001', 'completed', 'pickup', 2200.00, 2200.00, NOW()-INTERVAL '4 hours', NOW()-INTERVAL '2 hours'),
  (gen_random_uuid(), 'ORD-006', '{uid}', 'shop-001', 'completed', 'delivery', 1500.00, 1500.00, NOW()-INTERVAL '6 hours', NOW()-INTERVAL '3 hours')
ON CONFLICT DO NOTHING;
""")

# Delivery persons - using correct columns
psql("""
INSERT INTO delivery_persons (id, shop_id, name, phone, vehicle_number, is_active, current_status)
VALUES
  (gen_random_uuid(), 'shop-001', 'Muthu Krishnan', '+91 98765 43210', 'TN 01 AB 1234', true, 'available'),
  (gen_random_uuid(), 'shop-001', 'Selvam Raja', '+91 87654 32109', 'TN 02 CD 5678', true, 'available'),
  (gen_random_uuid(), 'shop-001', 'Kumar Vel', '+91 76543 21098', 'TN 03 EF 9812', true, 'available')
ON CONFLICT DO NOTHING;
""")

print("Done!")
