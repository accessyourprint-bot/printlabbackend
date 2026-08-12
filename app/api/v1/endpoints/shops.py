"""
Alt Print - Shops Management Endpoints
Create, read, update, delete, enable/disable shops
"""
import secrets
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.core.security import hash_password
from app.db.database import get_db
from app.models.models import FeatureFlag, Shop, User
from app.schemas.schemas import (
    APIResponse,
    CreateShopRequest,
    PaginatedResponse,
    ShopOut,
    UpdateShopRequest,
)
from app.services.audit import log_action

router = APIRouter(prefix="/shops", tags=["Shops"])

# Default feature flags created for each new shop
DEFAULT_SHOP_FEATURES = [
    ("black_white_print", "Black & White Printing"),
    ("color_print", "Color Printing"),
    ("spiral_binding", "Spiral Binding"),
    ("delivery", "Delivery"),
    ("front_back_printing", "Front/Back Printing"),
    ("bulk_orders", "Bulk Orders"),
    ("payment_upi", "UPI Payment"),
    ("payment_card", "Card Payment"),
    ("payment_cod", "Cash on Delivery"),
    ("login_register", "Login / Register"),
]


def _generate_shop_id(name: str, db_count: int) -> str:
    """Generate a human-readable shop ID"""
    return f"shop-{str(db_count + 1).zfill(3)}"


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_shop(
    body: CreateShopRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Create a new shop (Super Admin only)"""

    # Check email not already used
    existing = await db.execute(select(Shop).where(Shop.owner_email == body.owner_email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="A shop with this email already exists")

    # Generate shop ID
    all_shops = await db.execute(select(Shop))
    shop_count = len(all_shops.scalars().all())
    shop_id = body.id or _generate_shop_id(body.name, shop_count)

    # Check ID uniqueness
    id_check = await db.execute(select(Shop).where(Shop.id == shop_id))
    if id_check.scalar_one_or_none():
        shop_id = f"shop-{secrets.token_hex(3)}"

    shop = Shop(
        id=shop_id,
        name=body.name,
        owner_name=body.owner_name,
        owner_email=body.owner_email,
        owner_phone=body.owner_phone,
        address=body.address,
        city=body.city,
        state=body.state,
        pincode=body.pincode,
        latitude=body.latitude,
        longitude=body.longitude,
        delivery_radius_km=body.delivery_radius_km,
        is_active=True,
    )
    db.add(shop)
    await db.flush()

    # Create shop admin user account
    if body.admin_password:
        # Check if user exists for this email
        user_check = await db.execute(select(User).where(User.email == body.owner_email))
        existing_user = user_check.scalar_one_or_none()
        if not existing_user:
            shop_admin = User(
                email=body.owner_email,
                phone=body.owner_phone,
                hashed_password=hash_password(body.admin_password),
                full_name=body.owner_name,
                role="shop_admin",
                shop_id=shop_id,
                is_active=True,
            )
            db.add(shop_admin)

    # Create default shop-level feature flags (inherit from global by default)
    for feature_name, label in DEFAULT_SHOP_FEATURES:
        flag = FeatureFlag(
            feature_name=feature_name,
            label=label,
            enabled=True,
            scope="shop",
            shop_id=shop_id,
            updated_by=str(current_user.email),
        )
        db.add(flag)

    await db.flush()

    await log_action(
        db,
        actor=str(current_user.email),
        action="CREATE_SHOP",
        target=shop_id,
        details=body.name,
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(
        message=f"Shop '{body.name}' created successfully",
        data=ShopOut.model_validate(shop),
    )


@router.get("", response_model=List[ShopOut])
async def list_shops(
    active_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """List all shops"""
    query = select(Shop)
    if active_only:
        query = query.where(Shop.is_active == True)
    result = await db.execute(query.order_by(Shop.created_at))
    shops = result.scalars().all()
    return [ShopOut.model_validate(s) for s in shops]


@router.get("/{shop_id}", response_model=ShopOut)
async def get_shop(shop_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific shop by ID"""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return ShopOut.model_validate(shop)


@router.put("/{shop_id}", response_model=APIResponse)
async def update_shop(
    shop_id: str,
    body: UpdateShopRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update shop details"""
    # Shop admins can only edit their own shop
    if current_user.role == "shop_admin" and current_user.shop_id != shop_id:
        raise HTTPException(status_code=403, detail="Can only edit your own shop")
    elif current_user.role not in ("super_admin", "shop_admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(shop, field, value)

    await db.flush()

    await log_action(
        db,
        actor=str(current_user.email),
        action="UPDATE_SHOP",
        target=shop_id,
        details=body.model_dump(exclude_none=True),
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(message="Shop updated", data=ShopOut.model_validate(shop))


@router.patch("/{shop_id}/enable", response_model=APIResponse)
async def enable_shop(
    shop_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Enable a shop"""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    shop.is_active = True
    await db.flush()

    await log_action(db, str(current_user.email), "ENABLE_SHOP", shop_id,
                     details=shop.name, role=current_user.role, ip_address=get_client_ip(request))

    return APIResponse(message=f"Shop '{shop.name}' enabled")


@router.patch("/{shop_id}/disable", response_model=APIResponse)
async def disable_shop(
    shop_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Disable a shop"""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    shop.is_active = False
    await db.flush()

    await log_action(db, str(current_user.email), "DISABLE_SHOP", shop_id,
                     details=shop.name, role=current_user.role, ip_address=get_client_ip(request))

    return APIResponse(message=f"Shop '{shop.name}' disabled")


@router.delete("/{shop_id}", response_model=APIResponse)
async def delete_shop(
    shop_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    """Permanently delete a shop"""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    shop_name = shop.name
    await db.delete(shop)
    await db.flush()

    await log_action(db, str(current_user.email), "DELETE_SHOP", shop_id,
                     details=shop_name, role=current_user.role, ip_address=get_client_ip(request))

    return APIResponse(message=f"Shop '{shop_name}' deleted")


@router.patch("/{shop_id}/reset-password", response_model=APIResponse)
async def reset_shop_password(
    shop_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
    new_password: Optional[str] = Body(default=None, embed=True),
):
    """Reset the shop owner's login password to a new random password."""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    user_result = await db.execute(select(User).where(User.shop_id == shop_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="No login account found for this shop")

    if new_password:
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    else:
        new_password = secrets.token_urlsafe(9)
    user.hashed_password = hash_password(new_password)
    await db.flush()

    await log_action(db, str(current_user.email), "RESET_SHOP_PASSWORD", shop_id,
                     details=shop.name, role=current_user.role, ip_address=get_client_ip(request))
    return APIResponse(message=f"Password reset for '{shop.name}'", data={"new_password": new_password})
