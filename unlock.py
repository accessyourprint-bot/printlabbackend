import subprocess
r = subprocess.run(['docker','exec','altprint_postgres','psql','-U','altprint','-d','altprint_db','-c',
    "UPDATE users SET failed_login_attempts=0, locked_until=NULL WHERE email='admin@altprint.in'; SELECT email, failed_login_attempts, locked_until FROM users WHERE email='admin@altprint.in';"],
    capture_output=True,text=True)
print(r.stdout)
