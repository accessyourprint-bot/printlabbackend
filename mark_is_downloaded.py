import io

path = "app/api/v1/endpoints/files.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- FIX 1: mark is_downloaded on single-file download ----
old1 = """    except Exception:
        raise HTTPException(status_code=500, detail="Could not retrieve file")

    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type=order_file.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{order_file.original_filename}"'},
    )

@router.get("/orders/{order_id}/download-all")"""

new1 = """    except Exception:
        raise HTTPException(status_code=500, detail="Could not retrieve file")

    if order_file.order_id:
        mark_result = await db.execute(select(Order).where(Order.id == order_file.order_id))
        mark_order = mark_result.scalar_one_or_none()
        if mark_order and not mark_order.is_downloaded:
            mark_order.is_downloaded = True
            await db.commit()

    return StreamingResponse(
        io.BytesIO(file_bytes),
        media_type=order_file.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{order_file.original_filename}"'},
    )

@router.get("/orders/{order_id}/download-all")"""

c1 = content.count(old1)
print(f"Single-file download anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old1, new1)
    print("Single-file download now marks is_downloaded")
else:
    print("WARNING: anchor not found")

# ---- FIX 2: mark is_downloaded on download-all ----
old2 = """        raise HTTPException(status_code=404, detail="No files found for this order")

    zip_buffer = io.BytesIO()"""

new2 = """        raise HTTPException(status_code=404, detail="No files found for this order")

    if not order.is_downloaded:
        order.is_downloaded = True
        await db.commit()

    zip_buffer = io.BytesIO()"""

c2 = content.count(old2)
print(f"download-all anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old2, new2)
    print("download-all now marks is_downloaded")
else:
    print("WARNING: anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
