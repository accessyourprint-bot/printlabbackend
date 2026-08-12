import io

# --- 1. Add schema ---
path1 = "app/schemas/schemas.py"
with io.open(path1, "r", encoding="utf-8") as f:
    c1 = f.read()

old1 = """class RegisterRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\\+?[1-9]\\d{9,14}$")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None"""

new1 = old1 + """


class CreateShopLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    shop_id: str"""

n1 = c1.count(old1)
print(f"[schemas.py] RegisterRequest found {n1} time(s)")
if n1 == 1:
    c1 = c1.replace(old1, new1)
else:
    print("ABORT"); exit()
with io.open(path1, "w", encoding="utf-8") as f:
    f.write(c1)

# --- 2. Add endpoint in admin.py ---
path2 = "app/api/v1/endpoints/admin.py"
with io.open(path2, "r", encoding="utf-8") as f:
    c2 = f.read()

old2 = "from app.schemas.schemas import APIResponse, AdminOverviewOut, AdminUserOut, ShopOut, SystemConfigOut"
new2 = "from app.schemas.schemas import APIResponse, AdminOverviewOut, AdminUserOut, CreateShopLoginRequest, ShopOut, SystemConfigOut\nfrom app.core.security import hash_password"

n2 = c2.count(old2)
print(f"[admin.py] import line found {n2} time(s)")
if n2 == 1:
    c2 = c2.replace(old2, new2)
else:
    print("ABORT"); exit()

anchor = '@router.get("/users", response_model=list[AdminUserOut])'
new_endpoint = '''@router.post("/create-shop-login", response_model=APIResponse)
async def create_shop_login(
    body: CreateShopLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Create a proper shop_admin login account tied to a shop (used by Add Outlet)."""
    shop_result = await db.execute(select(Shop).where(Shop.id == body.shop_id))
    if not shop_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Shop not found")

    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="A login with this email already exists")

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
        role="shop_admin",
        shop_id=body.shop_id,
        is_active=True,
    )
    db.add(user)
    await db.flush()

    await log_action(
        db,
        actor=str(current_user.email),
        action="CREATE_SHOP_LOGIN",
        target=str(user.id),
        details={"shop_id": body.shop_id, "email": body.email},
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(message="Shop login created successfully")


@router.get("/users", response_model=list[AdminUserOut])'''

n3 = c2.count(anchor)
print(f"[admin.py] endpoint anchor found {n3} time(s)")
if n3 == 1:
    c2 = c2.replace(anchor, new_endpoint)
else:
    print("ABORT"); exit()
with io.open(path2, "w", encoding="utf-8") as f:
    f.write(c2)

print("Backend patch complete")
