import io

path = "app/api/v1/endpoints/files.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

anchor = """@router.delete("/{file_id}", response_model=APIResponse)
async def delete_file("""

new_endpoint = """@router.get("/orders/{order_id}/download-all")
async def download_all_files_for_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    \"\"\"Download all files for an order as a single zip. Owner, shop admin of that order's shop, or super admin only.\"\"\"
    import zipfile

    order_result = await db.execute(select(Order).where(Order.id == order_id))
    order = order_result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role == "user" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "shop_admin" and order.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")

    files_result = await db.execute(select(OrderFile).where(OrderFile.order_id == order_id))
    order_files = files_result.scalars().all()
    if not order_files:
        raise HTTPException(status_code=404, detail="No files found for this order")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        used_names = set()
        for f in order_files:
            try:
                file_bytes = await download_decrypted_file(f.storage_key, f.nonce)
            except Exception:
                continue
            name = f.original_filename or f"file_{f.id}"
            base_name = name
            counter = 1
            while name in used_names:
                stem, dot, ext = base_name.rpartition(".")
                name = f"{stem}_{counter}.{ext}" if dot else f"{base_name}_{counter}"
                counter += 1
            used_names.add(name)
            zf.writestr(name, file_bytes)

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{order.order_number}_documents.zip"'},
    )


@router.delete("/{file_id}", response_model=APIResponse)
async def delete_file("""

c = content.count(anchor)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(anchor, new_endpoint)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Bulk download-all-zip endpoint added")
else:
    print("WARNING: anchor not unique - manual fix needed")
