import subprocess, json

def psql(sql):
    r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c', sql], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

# Get admin user id
r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',"SELECT id FROM users WHERE email='admin@altprint.in';"], capture_output=True, text=True)
uid = r.stdout.strip()
print("Admin UID:", uid)

# Orders
psql(f"""
INSERT INTO orders (id, user_id, shop_id, status, product_name, copies, grand_total, created_at, completed_at)
VALUES
  (gen_random_uuid(), '{uid}', 'shop-001', 'printing', 'Business Cards', 500, 1200.00, NOW()-INTERVAL '2 hours', NULL),
  (gen_random_uuid(), '{uid}', 'shop-001', 'confirmed', 'Brochures A4', 200, 3500.00, NOW()-INTERVAL '1 hour', NULL),
  (gen_random_uuid(), '{uid}', 'shop-001', 'printing', 'Banners 3x6', 10, 4500.00, NOW()-INTERVAL '30 minutes', NULL),
  (gen_random_uuid(), '{uid}', 'shop-001', 'completed', 'Visiting Cards', 1000, 800.00, NOW()-INTERVAL '5 hours', NOW()-INTERVAL '1 hour'),
  (gen_random_uuid(), '{uid}', 'shop-001', 'completed', 'Flex Banner', 5, 2200.00, NOW()-INTERVAL '4 hours', NOW()-INTERVAL '2 hours'),
  (gen_random_uuid(), '{uid}', 'shop-001', 'completed', 'ID Cards', 50, 1500.00, NOW()-INTERVAL '6 hours', NOW()-INTERVAL '3 hours')
ON CONFLICT DO NOTHING;
""")

# Delivery persons
psql("""
INSERT INTO delivery_persons (id, shop_id, name, phone, age, aadhar_number, pan_number, vehicle_number, is_active)
VALUES
  (gen_random_uuid(), 'shop-001', 'Muthu Krishnan', '+91 98765 43210', 28, '1234 5678 9012', 'ABCDE1234F', 'TN 01 AB 1234', true),
  (gen_random_uuid(), 'shop-001', 'Selvam Raja', '+91 87654 32109', 32, '9876 5432 1098', 'FGHIJ5678K', 'TN 02 CD 5678', true),
  (gen_random_uuid(), 'shop-001', 'Kumar Vel', '+91 76543 21098', 25, '5678 9012 3456', 'LMNOP9012Q', 'TN 03 EF 9812', true)
ON CONFLICT DO NOTHING;
""")

# Stock items
psql("""
INSERT INTO stock_items (id, shop_id, item_name, quantity, unit, low_stock_threshold)
VALUES
  (gen_random_uuid(), 'shop-001', 'A4 Glossy Paper', 500, 'sheets', 50),
  (gen_random_uuid(), 'shop-001', 'A3 Matte Paper', 200, 'sheets', 30),
  (gen_random_uuid(), 'shop-001', 'Vinyl Roll 3ft', 8, 'rolls', 5),
  (gen_random_uuid(), 'shop-001', 'Flex Banner Material', 15, 'sqft', 10),
  (gen_random_uuid(), 'shop-001', 'Ink Cartridge Black', 12, 'units', 5),
  (gen_random_uuid(), 'shop-001', 'Ink Cartridge CMYK', 4, 'sets', 3),
  (gen_random_uuid(), 'shop-001', 'Lamination Film', 20, 'rolls', 5),
  (gen_random_uuid(), 'shop-001', 'Binding Wire', 30, 'boxes', 10)
ON CONFLICT DO NOTHING;
""")

# Tickets
psql(f"""
INSERT INTO support_tickets (id, shop_id, created_by, subject, description, status, priority)
VALUES
  (gen_random_uuid(), 'shop-001', '{uid}', 'Print quality issue', 'The color output on business cards is faded compared to the sample provided.', 'open', 'high'),
  (gen_random_uuid(), 'shop-001', '{uid}', 'Delivery delay', 'My order was supposed to arrive 3 days ago but still not received.', 'resolved', 'medium'),
  (gen_random_uuid(), 'shop-001', '{uid}', 'Machine breakdown', 'Large format printer stopped working mid-job.', 'open', 'high'),
  (gen_random_uuid(), 'shop-001', '{uid}', 'Stock shortage', 'Running low on A3 paper, need urgent restock.', 'open', 'medium')
ON CONFLICT DO NOTHING;
""")

print("All seed data inserted!")
