path = r"app\api\v1\endpoints\delivery.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

anchor = """@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])"""

new_endpoints = '''@router.post("/{person_id}/documents", response_model=DeliveryPersonOut)
async def upload_rider_document(
    person_id: str,
    doc_type: str = Form(..., pattern="^(driving_licence|vehicle_rc)$"),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Upload (or replace) a rider's driving licence or vehicle RC. Stored encrypted."""
    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")

    content_type = file.content_type or ""
    if content_type not in RIDER_DOC_ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WEBP, or PDF allowed")

    file_data = await file.read()
    if len(file_data) == 0:
        raise HTTPException(status_code=400, detail="Empty file not allowed")
    if len(file_data) > RIDER_DOC_MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large. Maximum size: 10MB")

    try:
        storage_key, nonce_hex = await upload_encrypted_file(
            file_data=file_data,
            original_filename=file.filename or doc_type,
            content_type=content_type,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if doc_type == "driving_licence":
        person.driving_licence_url = storage_key
        person.driving_licence_nonce = nonce_hex
    else:
        person.vehicle_rc_url = storage_key
        person.vehicle_rc_nonce = nonce_hex

    await db.commit()
    await db.refresh(person)
    return person


@router.get("/{person_id}/documents/{doc_type}/download")
async def download_rider_document(
    person_id: str,
    doc_type: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Download and decrypt a rider's driving licence or vehicle RC."""
    if doc_type not in ("driving_licence", "vehicle_rc"):
        raise HTTPException(status_code=400, detail="doc_type must be driving_licence or vehicle_rc")

    result = await db.execute(select(DeliveryPerson).where(DeliveryPerson.id == person_id))
    person = result.scalar_one_or_none()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    if current_user.role == "shop_admin" and person.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not authorized for this rider")

    storage_key = person.driving_licence_url if doc_type == "driving_licence" else person.vehicle_rc_url
    nonce_hex = person.driving_licence_nonce if doc_type == "driving_licence" else person.vehicle_rc_nonce

    if not storage_key or not nonce_hex:
        raise HTTPException(status_code=404, detail=f"No {doc_type} uploaded for this rider")

    file_bytes = await download_decrypted_file(storage_key, nonce_hex)
    return Response(content=file_bytes, media_type="application/octet-stream")


@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])'''

if src.count(anchor) != 1:
    raise SystemExit(f"FAILED: found {src.count(anchor)} matches for anchor, expected 1.")

src = src.replace(anchor, new_endpoints, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: document upload/download endpoints added.")
