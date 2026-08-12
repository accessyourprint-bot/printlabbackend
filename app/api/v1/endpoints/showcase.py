from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy import select, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, require_role
from app.db.database import get_db
from app.models.models import ShopShowcase, User
from app.schemas.schemas import APIResponse
from app.services.storage import delete_file_from_storage, download_decrypted_file, upload_encrypted_file

router = APIRouter(prefix="/showcase", tags=["Shop Showcase"])


class ShowcaseOut(BaseModel):
    id: UUID
    shop_id: str
    title: str
    original_filename: str
    content_type: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


@router.post("/upload", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def upload_showcase_item(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("shop_admin", "super_admin")),
):
    if not current_user.shop_id:
        raise HTTPException(status_code=400, detail="No shop associated with this account")

    file_data = await file.read()
    if len(file_data) == 0:
        raise HTTPException(status_code=400, detail="Empty file not allowed")

    content_type = file.content_type or "application/octet-stream"

    storage_key, nonce_hex = await upload_encrypted_file(
        file_data=file_data,
        original_filename=file.filename or "project",
        content_type=content_type,
    )

    item = ShopShowcase(
        shop_id=current_user.shop_id,
        title=title,
        storage_key=storage_key,
        nonce=nonce_hex,
        original_filename=file.filename or "project",
        content_type=content_type,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)

    return APIResponse(message="Project uploaded", data={"id": str(item.id)})


@router.get("", response_model=List[ShowcaseOut])
async def list_showcase_items(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(ShopShowcase).order_by(ShopShowcase.created_at.desc())
    if shop_id:
        q = q.where(ShopShowcase.shop_id == shop_id)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/mine", response_model=List[ShowcaseOut])
async def list_my_shop_showcase_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("shop_admin", "super_admin")),
):
    if not current_user.shop_id:
        return []
    q = select(ShopShowcase).where(ShopShowcase.shop_id == current_user.shop_id).order_by(ShopShowcase.created_at.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{item_id}/download")
async def download_showcase_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    from fastapi.responses import StreamingResponse
    import io as _io

    result = await db.execute(select(ShopShowcase).where(ShopShowcase.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")

    file_bytes = await download_decrypted_file(item.storage_key, item.nonce)
    return StreamingResponse(
        _io.BytesIO(file_bytes),
        media_type=item.content_type,
        headers={"Content-Disposition": f"attachment; filename=\"{item.original_filename}\""},
    )


@router.delete("/{item_id}", response_model=APIResponse)
async def delete_showcase_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("shop_admin", "super_admin")),
):
    result = await db.execute(select(ShopShowcase).where(ShopShowcase.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.role != "super_admin" and item.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    await delete_file_from_storage(item.storage_key)
    await db.execute(sa_delete(ShopShowcase).where(ShopShowcase.id == item_id))
    await db.commit()
    return APIResponse(message="Deleted")
