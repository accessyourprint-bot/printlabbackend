from passlib.context import CryptContext
import subprocess
pwd = CryptContext(schemes=['bcrypt'])
h = pwd.hash('Admin@1234')
print('Hash:', h[:20]+'...')
r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c',f"UPDATE users SET hashed_password = '{h}' WHERE email='admin@altprint.in';"],capture_output=True,text=True)
print(r.stdout.strip(), r.stderr.strip())
