import subprocess
h = '$2b$12$5wULwW3U6uqw6Qog5RvgzumJg1FudWDAiBgmnMevHm/N0zMvKgZta'
r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c',f"UPDATE users SET hashed_password = '{h}' WHERE email='admin@altprint.in';"],capture_output=True,text=True)
print(r.stdout, r.stderr)
