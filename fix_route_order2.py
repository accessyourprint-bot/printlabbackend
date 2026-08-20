path = r"app\api\v1\endpoints\delivery.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

me_block = """@router.get("/me", response_model=DeliveryPersonOut)
async def get_my_rider_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    \"\"\"Rider app calls this after login to get its own profile.\"\"\"
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.user_id == current_user.id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="No rider profile linked to this account")
    return person


"""

if src.count(me_block) != 1:
    raise SystemExit(f"FAILED: could not find /me block to move, found {src.count(me_block)} times.")

src = src.replace(me_block, "", 1)

anchor = """@router.get("/{person_id}", response_model=DeliveryPersonOut)"""
if src.count(anchor) != 1:
    raise SystemExit(f"FAILED: could not find anchor, found {src.count(anchor)} times.")

src = src.replace(anchor, me_block + anchor, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: /me route moved above /{person_id}.")
