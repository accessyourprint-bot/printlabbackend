import subprocess

def psql(sql):
    r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c', sql], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',"SELECT id FROM users WHERE email='admin@altprint.in';"], capture_output=True, text=True)
uid = r.stdout.strip()

psql(f"""
INSERT INTO orders (id, order_number, user_id, shop_id, status, delivery_type, grand_total, printing_cost, created_at, completed_at)
VALUES
  (gen_random_uuid(), 'ORD-A001', '{uid}', 'shop-001', 'processing', 'self_pickup', 1200.00, 1200.00, NOW()-INTERVAL '2 hours', NULL),
  (gen_random_uuid(), 'ORD-A002', '{uid}', 'shop-001', 'confirmed',  'self_pickup', 3500.00, 3500.00, NOW()-INTERVAL '1 hour', NULL),
  (gen_random_uuid(), 'ORD-A003', '{uid}', 'shop-001', 'processing', 'home_delivery', 4500.00, 4500.00, NOW()-INTERVAL '30 minutes', NULL),
  (gen_random_uuid(), 'ORD-A004', '{uid}', 'shop-001', 'delivered',  'self_pickup', 800.00, 800.00, NOW()-INTERVAL '5 hours', NOW()-INTERVAL '1 hour'),
  (gen_random_uuid(), 'ORD-A005', '{uid}', 'shop-001', 'delivered',  'self_pickup', 2200.00, 2200.00, NOW()-INTERVAL '4 hours', NOW()-INTERVAL '2 hours'),
  (gen_random_uuid(), 'ORD-A006', '{uid}', 'shop-001', 'delivered',  'home_delivery', 1500.00, 1500.00, NOW()-INTERVAL '6 hours', NOW()-INTERVAL '3 hours')
ON CONFLICT DO NOTHING;
""")

# Get the new order IDs
r3 = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-t','-c',
    "SELECT id FROM orders WHERE order_number LIKE 'ORD-A%' ORDER BY created_at;"],
    capture_output=True, text=True)
oids = [x.strip() for x in r3.stdout.strip().split('\n') if x.strip()]
print("Order IDs:", oids)

files = [
    ('Business_Cards.pdf', 500),
    ('Brochures_A4.pdf', 200),
    ('Banner_3x6.pdf', 10),
    ('Visiting_Cards.pdf', 1000),
    ('Flex_Banner.pdf', 5),
    ('ID_Cards.pdf', 50),
]

for oid, (fname, copies) in zip(oids, files):
    psql(f"""
INSERT INTO order_files (id, order_id, user_id, storage_key, nonce, original_filename, content_type, file_size_bytes, page_count, file_type, print_color, copies, is_front_back, file_cost, status, expires_at)
VALUES (gen_random_uuid(), '{oid}', '{uid}', 'store/{oid[:8]}/{fname}', 'nc{oid[:8]}', '{fname}', 'application/pdf', 102400, 1, 'document', 'color', {copies}, false, 500.00, 'printed', NOW()+INTERVAL '30 days')
ON CONFLICT DO NOTHING;
""")

print("Orders + files done!")
