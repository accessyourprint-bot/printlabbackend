"""
Alt Print - File Upload Endpoints
Secure upload with AES-256 encryption, page counting, auto-delete scheduling
"""
from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.core.config import settings
from app.db.database import get_db
from app.models.models import Order, OrderFile, SystemConfig, User
from fastapi.responses import StreamingResponse
import io
from app.schemas.schemas import APIResponse, FileCustomization, OrderFileOut
from app.services.page_counter import count_pages
from app.services.storage import delete_file_from_storage, download_decrypted_file, upload_encrypted_file

router = APIRouter(prefix="/files", tags=["Files"])

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "image/png",
    "image/jpeg",
    "image/jpg",
}


async def _check_uploads_enabled(db: AsyncSession) -> None:
    result = await db.execute(select(SystemConfig).where(SystemConfig.id == 1))
    config = result.scalar_one_or_none()
    if config and (not config.uploads_enabled or config.emergency_lock or not config.app_enabled):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="File uploads are currently disabled",
        )


@router.post("/upload", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    print_color: str = Form("black_white"),
    copies: int = Form(1),
    is_front_back: bool = Form(False),
    spiral_binding: bool = Form(False),
    colored_binding_sheet: bool = Form(False),
    custom_instructions: str = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload and encrypt a document.
    File is AES-256-GCM encrypted before storage.
    Original filename is never stored in S3/R2.
    """
    await _check_uploads_enabled(db)

    # Validate file type
    content_type = file.content_type or ""
    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else ""

    if content_type not in ALLOWED_CONTENT_TYPES and ext not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(settings.allowed_extensions_list)}",
        )

    # Read and size check
    file_data = await file.read()
    if len(file_data) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB",
        )

    if len(file_data) == 0:
        raise HTTPException(status_code=400, detail="Empty file not allowed")

    # Count pages
    page_count, file_type = await count_pages(file_data, file.filename or "file", content_type)

    # Validate customization
    customization = FileCustomization(
        print_color=print_color,
        copies=copies,
        is_front_back=is_front_back,
        spiral_binding=spiral_binding,
        colored_binding_sheet=colored_binding_sheet,
        custom_instructions=custom_instructions,
    )

    # Encrypt and upload to S3/R2
    try:
        storage_key, nonce_hex = await upload_encrypted_file(
            file_data=file_data,
            original_filename=file.filename or "document",
            content_type=content_type,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save metadata (never save original path or plaintext filename in storage)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.FILE_RETENTION_DAYS)

    order_file = OrderFile(
        user_id=current_user.id,
        storage_key=storage_key,
        nonce=nonce_hex,
        original_filename=file.filename or "document",
        content_type=content_type,
        file_size_bytes=len(file_data),
        page_count=page_count,
        file_type=file_type,
        print_color=customization.print_color,
        copies=customization.copies,
        is_front_back=customization.is_front_back,
        spiral_binding=customization.spiral_binding,
        colored_binding_sheet=customization.colored_binding_sheet,
        custom_instructions=customization.custom_instructions,
        status="uploaded",
        expires_at=expires_at,
    )
    db.add(order_file)
    await db.flush()
    await db.refresh(order_file)

    return APIResponse(
        message="File uploaded successfully",
        data={
            "file_id": str(order_file.id),
            "original_filename": order_file.original_filename,
            "page_count": page_count,
            "file_type": file_type,
            "expires_at": expires_at.isoformat(),
        },
    )


@router.post("/upload/multiple", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload multiple files at once. Returns list of file IDs with page counts."""
    await _check_uploads_enabled(db)

    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files per upload")

    results = []
    for file in files:
        content_type = file.content_type or ""
        ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else ""

        if content_type not in ALLOWED_CONTENT_TYPES and ext not in settings.allowed_extensions_list:
            results.append({
                "filename": file.filename,
                "error": "File type not allowed",
                "success": False,
            })
            continue

        file_data = await file.read()
        if len(file_data) > settings.max_file_size_bytes:
            results.append({
                "filename": file.filename,
                "error": f"File too large (max {settings.MAX_FILE_SIZE_MB}MB)",
                "success": False,
            })
            continue

        page_count, file_type = await count_pages(file_data, file.filename or "file", content_type)

        try:
            storage_key, nonce_hex = await upload_encrypted_file(
                file_data=file_data,
                original_filename=file.filename or "document",
                content_type=content_type,
            )
        except RuntimeError as e:
            results.append({"filename": file.filename, "error": str(e), "success": False})
            continue

        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.FILE_RETENTION_DAYS)
        order_file = OrderFile(
            user_id=current_user.id,
            storage_key=storage_key,
            nonce=nonce_hex,
            original_filename=file.filename or "document",
            content_type=content_type,
            file_size_bytes=len(file_data),
            page_count=page_count,
            file_type=file_type,
            print_color="black_white",
            copies=1,
            status="uploaded",
            expires_at=expires_at,
        )
        db.add(order_file)
        await db.flush()
        await db.refresh(order_file)

        results.append({
            "file_id": str(order_file.id),
            "filename": file.filename,
            "page_count": page_count,
            "file_type": file_type,
            "success": True,
        })

    total_pages = sum(r.get("page_count", 0) for r in results if r.get("success"))
    return APIResponse(
        message=f"Uploaded {sum(1 for r in results if r.get('success'))} of {len(files)} files",
        data={"files": results, "total_pages": total_pages},
    )


@router.get("/my", response_model=List[OrderFileOut])
async def list_my_files(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List current user's uploaded files"""
    result = await db.execute(
        select(OrderFile).where(
            OrderFile.user_id == current_user.id,
            OrderFile.deleted_at == None,
            OrderFile.status != "deleted",
        ).order_by(OrderFile.created_at.desc())
    )
    files = result.scalars().all()
    return [OrderFileOut.model_validate(f) for f in files]


@router.get("/{file_id}/download")
async def download_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download and decrypt a file. Owner, shop admin of that order's shop, or super admin only."""
    result = await db.execute(select(OrderFile).where(OrderFile.id == file_id))
    order_file = result.scalar_one_or_none()
    if not order_file:
        raise HTTPException(status_code=404, detail="File not found")

    if current_user.role == "user" and order_file.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "shop_admin":
        if not order_file.order_id:
            raise HTTPException(status_code=403, detail="Access denied")
        order_result = await db.execute(select(Order).where(Order.id == order_file.order_id))
        order = order_result.scalar_one_or_none()
        if not order or order.shop_id != current_user.shop_id:
            raise HTTPException(status_code=403, detail="Access denied")

    try:
        file_bytes = await download_decrypted_file(order_file.storage_key, order_file.nonce)
    except Exception:
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

@router.get("/orders/{order_id}/download-all")
async def download_all_files_for_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download all files for an order as a single zip. Owner, shop admin of that order's shop, or super admin only."""
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

    if not order.is_downloaded:
        order.is_downloaded = True
        await db.commit()

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
async def delete_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a file (user can only delete their own files)"""
    result = await db.execute(
        select(OrderFile).where(
            OrderFile.id == file_id,
            OrderFile.user_id == current_user.id,
        )
    )
    order_file = result.scalar_one_or_none()

    if not order_file:
        raise HTTPException(status_code=404, detail="File not found")

    if order_file.status == "deleted":
        raise HTTPException(status_code=400, detail="File already deleted")

    # Delete from storage
    await delete_file_from_storage(order_file.storage_key)

    # Mark as deleted
    order_file.status = "deleted"
    order_file.deleted_at = datetime.now(timezone.utc)
    await db.flush()

    return APIResponse(message="File deleted successfully")
