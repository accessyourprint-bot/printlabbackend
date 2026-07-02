import subprocess, bcrypt
pw = b"Admin123!"
h = bcrypt.hashpw(pw, bcrypt.gensalt(12)).decode()
r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c',f"UPDATE users SET hashed_password='{h}' WHERE email='admin@altprint.in';"],capture_output=True,text=True)
print("Password set to: Admin123!")
print(r.stdout, r.stderr)
