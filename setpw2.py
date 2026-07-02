import subprocess, bcrypt

# Set new password
pw = b"Admin123!"
h = bcrypt.hashpw(pw, bcrypt.gensalt(12)).decode()
subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c',
    f"UPDATE users SET hashed_password='{h}' WHERE email='admin@altprint.in';"],capture_output=True,text=True)

# Verify it works
stored = h.encode()
print("Hash set. Verify:", bcrypt.checkpw(pw, stored))
print("Hash:", h)
