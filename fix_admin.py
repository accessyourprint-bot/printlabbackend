import subprocess
from passlib.context import CryptContext
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
new_hash = pwd_ctx.hash("Admin@1234")
sql = f"UPDATE users SET hashed_password = '{new_hash}', is_active = true WHERE email = 'admin@altprint.in';"
r = subprocess.run(
    ["docker", "exec", "altprint_postgres", "psql", "-U", "altprint", "-d", "altprint_db", "-c", sql],
    capture_output=True, text=True
)
print("STDOUT:", r.stdout)
print("STDERR:", r.stderr)
print("Done. Try logging in with Admin@1234")
