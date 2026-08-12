import io

# --- 1. Update schema ---
path1 = "app/schemas/schemas.py"
with io.open(path1, "r", encoding="utf-8") as f:
    c1 = f.read()

old1 = """class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    role: str
    user_id: str"""

new1 = """class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    role: str
    user_id: str
    shop_id: Optional[str] = None"""

n1 = c1.count(old1)
print(f"[schemas.py] TokenResponse found {n1} time(s)")
if n1 == 1:
    c1 = c1.replace(old1, new1)
else:
    print("ABORT: schema anchor mismatch"); exit()
with io.open(path1, "w", encoding="utf-8") as f:
    f.write(c1)

# --- 2. Update auth.py: both TokenResponse(...) calls ---
path2 = "app/api/v1/endpoints/auth.py"
with io.open(path2, "r", encoding="utf-8") as f:
    c2 = f.read()

old2a = """    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        role=user.role,
        user_id=str(user.id),
    )"""
new2a = """    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        role=user.role,
        user_id=str(user.id),
        shop_id=user.shop_id,
    )"""

old2b = """    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        role=user.role,
        user_id=str(user.id),
    )"""
new2b = """    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        role=user.role,
        user_id=str(user.id),
        shop_id=user.shop_id,
    )"""

n2a = c2.count(old2a)
n2b = c2.count(old2b)
print(f"[auth.py] login return found {n2a} time(s), refresh return found {n2b} time(s)")
if n2a == 1 and n2b == 1:
    c2 = c2.replace(old2a, new2a).replace(old2b, new2b)
else:
    print("ABORT: auth.py anchor mismatch"); exit()
with io.open(path2, "w", encoding="utf-8") as f:
    f.write(c2)

print("Backend patch complete")
