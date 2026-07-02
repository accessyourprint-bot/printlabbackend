import subprocess
r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c',"SELECT email, hashed_password, is_active, role FROM users WHERE email='admin@altprint.in';"],capture_output=True,text=True)
print(r.stdout)
print(r.stderr)
