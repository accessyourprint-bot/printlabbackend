# Final fix: reset passwords to match hardcoded form defaults,
# and prevent Sign In double-clicks.

import subprocess

# 1. Generate correct hashes for the hardcoded default passwords
result = subprocess.run(
    ["docker", "exec", "altprint_api", "python", "-c",
     "from app.core.security import hash_password; print(hash_password('Shop1234!'))"],
    capture_output=True, text=True
)
shop_hash = result.stdout.strip()
print("Shop hash:", shop_hash, result.stderr)

result2 = subprocess.run(
    ["docker", "exec", "altprint_api", "python", "-c",
     "from app.core.security import hash_password; print(hash_password('Admin123!'))"],
    capture_output=True, text=True
)
admin_hash = result2.stdout.strip()
print("Admin hash:", admin_hash, result2.stderr)

# 2. Write SQL update file
with open("update_passwords.sql", "w") as f:
    f.write(f"UPDATE users SET hashed_password = '{shop_hash}' WHERE email = 'shop@altprint.in';\n")
    f.write(f"UPDATE users SET hashed_password = '{admin_hash}' WHERE email = 'admin@altprint.in';\n")

print("Wrote update_passwords.sql -- now run the docker cp + psql commands shown next.")