"""
Alt Print - Stock Management Endpoints
Shop admins manage their own shop stock; super admin manages all shops.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import StockItem, User
from app.schemas.schemas import APIResponse, StockItemCreate, StockItemOut, StockItemUpdate

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.get("", response_model=List[StockItemOut])
async def list_stock(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """List stock items. Shop admins see only their shop; super admin can filter by shop_id."""
    query = select(StockItem)
    if current_user.role == "shop_admin":
        query = query.where(StockItem.shop_id == current_user.shop_id)
    elif shop_id:
        query = query.where(StockItem.shop_id == shop_id)

    result = await db.execute(query.order_by(StockItem.item_name))
    items = result.scalars().all()
    return [StockItemOut.model_validate(i) for i in items]


@router.post("", response_model=APIResponse, status_code=201)
async def create_stock_item(
    body: StockItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Add a new stock item."""
    shop_id = current_user.shop_id if current_user.role == "shop_admin" else body.shop_id
    if not shop_id:
        raise HTTPException(status_code=400, detail="shop_id is required")

    item = StockItem(
        shop_id=shop_id,
        item_name=body.item_name,
        quantity=body.quantity,
        unit=body.unit,
        low_stock_threshold=body.low_stock_threshold,
        updated_by=current_user.id,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return APIResponse(message="Stock item created", data={"id": str(item.id)})


@router.patch("/{item_id}", response_model=APIResponse)
async def update_stock_item(
    item_id: str,
    body: StockItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Update quantity, unit, or low-stock threshold."""
    result = await db.execute(select(StockItem).where(StockItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Stock item not found")
    if current_user.role == "shop_admin" and item.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if body.quantity is not None:
        item.quantity = body.quantity
    if body.unit is not None:
        item.unit = body.unit
    if body.low_stock_threshold is not None:
        item.low_stock_threshold = body.low_stock_threshold
    item.updated_by = current_user.id

    await db.flush()
    return APIResponse(message="Stock item updated", data={"id": item_id, "quantity": item.quantity})


@router.delete("/{item_id}", response_model=APIResponse)
async def delete_stock_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    """Remove a stock item."""
    result = await db.execute(select(StockItem).where(StockItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Stock item not found")
    if current_user.role == "shop_admin" and item.shop_id != current_user.shop_id:
        raise HTTPException(status_code=403, detail="Access denied")

    await db.delete(item)
    await db.flush()
    return APIResponse(message="Stock item deleted", data={"id": item_id})
