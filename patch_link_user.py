path = r"app\api\v1\endpoints\delivery.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

anchor = """@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])"""

new_endpoints = '''@router.get("/me", response_model=DeliveryPersonOut)
async def get_my_rider_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Rider app calls this after login to get its own profile."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == current_user.id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="No rider profile linked to this account")
    return person


@router.patch("/{person_id}/link-user", response_model=DeliveryPersonOut)
async def link_delivery_person_to_user(
    person_id: str,
    phone: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Link an existing delivery person to a login-capable user account by phone.
    Finds or creates the User, sets role=rider, and links delivery_persons.user_id."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")

    user_result = await db.execute(select(User).where(User.phone == phone))
    linked_user = user_result.scalar_one_or_none()

    if linked_user:
        if linked_user.role not in ("rider", "user"):
            raise HTTPException(status_code=400, detail=f"Phone already belongs to a {linked_user.role} account")
        linked_user.role = "rider"
    else:
        import uuid as _uuid
        linked_user = User(id=_uuid.uuid4(), phone=phone, role="rider", full_name=person.name, is_active=True, is_verified=True)
        db.add(linked_user)
        await db.flush()

    existing_link = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == linked_user.id))
    if existing_link.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="This phone is already linked to another rider profile")

    person.user_id = linked_user.id
    await db.commit()
    await db.refresh(person)
    return person


@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])'''

if src.count(anchor) != 1:
    raise SystemExit(f"FAILED: found {src.count(anchor)} matches for anchor, expected 1.")

src = src.replace(anchor, new_endpoints, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: /me and /link-user endpoints added.")
