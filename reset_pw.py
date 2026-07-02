from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
h = pwd_context.hash("Admin123!")
with open("reset_pw.sql", "w") as f:
    f.write("UPDATE users SET hashed_password = '" + h + "', failed_login_attempts = 0, locked_until = NULL WHERE email = 'admin@altprint.in';")
print("Hash written to reset_pw.sql:", h)
