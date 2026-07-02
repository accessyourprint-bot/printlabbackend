from passlib.context import CryptContext
import bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
h = "$2b$12$8CofR3ebQZmR1yjWGDTsKuGzzce44kychS0VL5VD8nagGslS7pcui"
print("passlib verify Admin123!:", pwd_context.verify("Admin123!", h))
print("bcrypt verify Admin123!:", bcrypt.checkpw(b"Admin123!", h.encode()))
