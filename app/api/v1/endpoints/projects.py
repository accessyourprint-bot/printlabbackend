"""
Alt Print - Projects Endpoints
Project upload/list/print wrappers built on the existing encrypted file and order flow.
"""
from typing import List

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.models.models import OrderFile, SystemConfig, User
from app.schemas.schemas import APIResponse, FileCustomization, OrderFileOut, ProjectPrintRequest
from app.services.page_counter import count_pages
from app.services.storage import upload_encrypted_file
from app.api.v1.endpoints.orders import create_order

router = APIRouter(prefix="/projects", tags=["Projects"])


async def _check_uploads_enabled(db: AsyncSession) -> None:
    result = await db.execute(select(SystemConfig).where(SystemConfig.id == 1))
    config = result.scalar_one_or_none()
    if config and (not config.uploads_enabled or config.emergency_lock or not config.app_enabled):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Project uploads are currently disabled",
        )


@router.post("/upload", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def upload_project(
    file: UploadFile = File(...),
    print_color: str = Form("black_white"),
    copies: int = Form(1),
    is_front_back: bool = Form(False),
    spiral_binding: bool = Form(False),
    colored_binding_sheet: bool = Form(False),
    custom_instructions: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a project file using the existing encrypted storage flow."""
    await _check_uploads_enabled(db)

    content_type = file.content_type or ""
    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else ""

    if content_type not in {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword", "image/png", "image/jpeg", "image/jpg"} and ext not in settings.allowed_extensions_list:
        raise HTTPException(status_code=400, detail=f"File type not allowed. Supported: {', '.join(settings.allowed_extensions_list)}")

    file_data = await file.read()
    if len(file_data) > settings.max_file_size_bytes:
        raise HTTPException(status_code=413, detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB")
    if len(file_data) == 0:
        raise HTTPException(status_code=400, detail="Empty file not allowed")

    page_count, file_type = await count_pages(file_data, file.filename or "file", content_type)
    storage_key, nonce_hex = await upload_encrypted_file(file_data, file.filename or "document", content_type)

    order_file = OrderFile(
        user_id=current_user.id,
        storage_key=storage_key,
        nonce=nonce_hex,
        original_filename=file.filename or "document",
        content_type=content_type,
        file_size_bytes=len(file_data),
        page_count=page_count,
        file_type=file_type,
        print_color=print_color,
        copies=copies,
        is_front_back=is_front_back,
        spiral_binding=spiral_binding,
        colored_binding_sheet=colored_binding_sheet,
        custom_instructions=custom_instructions,
        status="pending_approval",
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.FILE_RETENTION_DAYS),
    )

    db.add(order_file)
    await db.flush()
    await db.refresh(order_file)

    return APIResponse(
        message="Project uploaded successfully",
        data={
            "project_id": str(order_file.id),
            "original_filename": order_file.original_filename,
            "page_count": page_count,
            "file_type": file_type,
        },
    )


@router.get("", response_model=List[OrderFileOut])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List the current user's uploaded projects."""
    result = await db.execute(
        select(OrderFile).where(
            OrderFile.user_id == current_user.id,
            OrderFile.deleted_at == None,
            OrderFile.status != "deleted",
        ).order_by(OrderFile.created_at.desc())
    )
    files = result.scalars().all()
    return [OrderFileOut.model_validate(f) for f in files]


@router.post("/print", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def print_project(
    body: ProjectPrintRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create an order from uploaded project files."""
    if not body.file_customizations:
        body.file_customizations = {str(file_id): FileCustomization() for file_id in body.file_ids}
    return await create_order(body, request, db, current_user)