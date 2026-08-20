path = r"app\api\v1\endpoints\delivery.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

anchor = '''@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])'''

new_endpoint = '''@router.get("/{person_id}", response_model=DeliveryPersonOut)
async def get_delivery_person(
    person_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Full profile for a single delivery person (rider details page)."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")
    return person


@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])'''

if src.count(anchor) != 1:
    raise SystemExit(f"FAILED: found {src.count(anchor)} matches for anchor in delivery.py, expected 1.")

src = src.replace(anchor, new_endpoint, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: GET /delivery-persons/{person_id} endpoint added.")
