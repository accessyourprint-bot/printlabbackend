import subprocess, bcrypt
r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c',
    "SELECT hashed_password FROM users WHERE email='admin@altprint.in';"],capture_output=True,text=True)
h = r.stdout.strip().split('\n')[2].strip().encode()
print("Hash in DB:", h)
print("Match AltPrint2024!:", bcrypt.checkpw(b"AltPrint2024!", h))
