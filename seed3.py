import subprocess

def psql(sql):
    r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c', sql], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',"SELECT id FROM users WHERE email='admin@altprint.in';"], capture_output=True, text=True)
uid = r.stdout.strip()
print("UID:", uid)

# Orders with correct status values
psql(f"""
INSERT INTO orders (id, order_number, user_id, shop_id, status, delivery_type, grand_total, printing_cost, created_at, completed_at)
VALUES
  (gen_random_uuid(), 'ORD-001', '{uid}', 'shop-001', 'processing', 'pickup', 1200.00, 1200.00, NOW()-INTERVAL '2 hours', NULL),
  (gen_random_uuid(), 'ORD-002', '{uid}', 'shop-001', 'confirmed', 'pickup', 3500.00, 3500.00, NOW()-INTERVAL '1 hour', NULL),
  (gen_random_uuid(), 'ORD-003', '{uid}', 'shop-001', 'processing', 'delivery', 4500.00, 4500.00, NOW()-INTERVAL '30 minutes', NULL),
  (gen_random_uuid(), 'ORD-004', '{uid}', 'shop-001', 'delivered', 'pickup', 800.00, 800.00, NOW()-INTERVAL '5 hours', NOW()-INTERVAL '1 hour'),
  (gen_random_uuid(), 'ORD-005', '{uid}', 'shop-001', 'delivered', 'pickup', 2200.00, 2200.00, NOW()-INTERVAL '4 hours', NOW()-INTERVAL '2 hours'),
  (gen_random_uuid(), 'ORD-006', '{uid}', 'shop-001', 'delivered', 'delivery', 1500.00, 1500.00, NOW()-INTERVAL '6 hours', NOW()-INTERVAL '3 hours')
ON CONFLICT DO NOTHING;
""")

# Order files (product names) - link to the orders we just created
r2 = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',
    "SELECT id, order_number FROM orders ORDER BY created_at DESC LIMIT 6;"],
    capture_output=True, text=True)
print("Orders:", r2.stdout.strip())

# Get order IDs
r3 = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',
    "SELECT id FROM orders ORDER BY created_at DESC LIMIT 6;"],
    capture_output=True, text=True)
oids = [x.strip() for x in r3.stdout.strip().split('\n') if x.strip()]

files = [
    ('Business Cards.pdf', 500),
    ('Brochures_A4.pdf', 200),
    ('Banner_3x6.pdf', 10),
    ('Visiting_Cards.pdf', 1000),
    ('Flex_Banner.pdf', 5),
    ('ID_Cards.pdf', 50),
]

for oid, (fname, copies) in zip(oids, files):
    psql(f"""
INSERT INTO order_files (id, order_id, user_id, storage_key, nonce, original_filename, content_type, file_size_bytes, page_count, file_type, print_color, copies, is_front_back, file_cost, status, expires_at)
VALUES (gen_random_uuid(), '{oid}', '{uid}', 'store/{oid}/{fname}', 'nonce{oid[:8]}', '{fname}', 'application/pdf', 102400, 1, 'document', 'color', {copies}, false, 500.00, 'printed', NOW()+INTERVAL '30 days')
ON CONFLICT DO NOTHING;
""")

# Extra stock items
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

# Extra tickets
psql(f"""
INSERT INTO support_tickets (id, shop_id, created_by, subject, description, status, priority)
VALUES
  (gen_random_uuid(), 'shop-001', '{uid}', 'Print quality issue', 'Color output on business cards is faded.', 'open', 'high'),
  (gen_random_uuid(), 'shop-001', '{uid}', 'Delivery delay', 'Order was supposed to arrive 3 days ago.', 'resolved', 'medium'),
  (gen_random_uuid(), 'shop-001', '{uid}', 'Machine breakdown', 'Large format printer stopped mid-job.', 'open', 'high'),
  (gen_random_uuid(), 'shop-001', '{uid}', 'Stock shortage', 'Running low on A3 paper, need urgent restock.', 'open', 'medium')
ON CONFLICT DO NOTHING;
""")

print("All done!")
