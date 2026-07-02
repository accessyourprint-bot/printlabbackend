"""
Alt Print - Analytics, Pricing, Earnings, Live Monitor (Features 5-11)
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func as sqlfunc
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import Order, PrintPricing, Shop, ShopEarnings, User
from app.schemas.schemas import APIResponse, PricingCreate, PricingOut, ShopEarningsOut

router = APIRouter(prefix="/analytics", tags=["Analytics"])
pricing_router = APIRouter(prefix="/pricing", tags=["Pricing"])


# ── FEATURE 5: Price Control ──────────────────────────────────────────────────

@pricing_router.get("", response_model=List[PricingOut])
async def list_pricing(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    result = await db.execute(select(PrintPricing))
    items = result.scalars().all()
    return [PricingOut.model_validate(i) for i in items]


@pricing_router.post("", response_model=APIResponse, status_code=201)
async def set_pricing(
    body: PricingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    item = PrintPricing(
        print_type=body.print_type,
        price_per_page=body.price_per_page,
        shop_id=body.shop_id,
        is_global=body.is_global,
        updated_by=current_user.id,
    )
    db.add(item)
    await db.flush()
    return APIResponse(message="Pricing set", data={"print_type": body.print_type, "price": body.price_per_page})


@pricing_router.patch("/{pricing_id}", response_model=APIResponse)
async def update_pricing(
    pricing_id: str,
    price_per_page: float,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    result = await db.execute(select(PrintPricing).where(PrintPricing.id == pricing_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Pricing not found")
    item.price_per_page = price_per_page
    item.updated_by = current_user.id
    await db.flush()
    return APIResponse(message="Pricing updated", data={"id": pricing_id, "price": price_per_page})


# ── FEATURE 8: Outlet Job Monitoring + Earnings ───────────────────────────────

@router.get("/shop-earnings", response_model=List[ShopEarningsOut])
async def shop_earnings(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    query = select(Order)
    if current_user.role == "shop_admin":
        query = query.where(Order.shop_id == current_user.shop_id)
    elif shop_id:
        query = query.where(Order.shop_id == shop_id)

    result = await db.execute(query)
    orders = result.scalars().all()

    shops_map = {}
    for o in orders:
        sid = o.shop_id
        if sid not in shops_map:
            shops_map[sid] = {"shop_id": sid, "total_earnings": 0.0, "order_count": 0, "jobs_done": 0}
        shops_map[sid]["total_earnings"] += o.grand_total or 0
        shops_map[sid]["order_count"] += 1
        if o.status in ("completed", "delivered"):
            shops_map[sid]["jobs_done"] += 1

    return [ShopEarningsOut(**v) for v in shops_map.values()]


# ── FEATURE 9: Total Jobs Done + Live Job Monitor ─────────────────────────────

@router.get("/live-jobs")
async def live_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    query = select(Order)
    if current_user.role == "shop_admin":
        query = query.where(Order.shop_id == current_user.shop_id)

    result = await db.execute(query)
    orders = result.scalars().all()

    statuses = {}
    for o in orders:
        statuses[o.status] = statuses.get(o.status, 0) + 1

    return {
        "total_orders": len(orders),
        "by_status": statuses,
        "live_active": [
            {"id": str(o.id), "order_number": o.order_number, "status": o.status,
             "shop_id": o.shop_id, "amount": o.grand_total}
            for o in orders if o.status in ("confirmed", "printing", "ready", "out_for_delivery")
        ]
    }


# ── FEATURE 10: Multiple Admin Roles ─────────────────────────────────────────

@router.get("/role-summary")
async def role_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin")),
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    roles = {}
    for u in users:
        roles[u.role] = roles.get(u.role, 0) + 1
    return {"total_users": len(users), "by_role": roles, "users": [
        {"id": str(u.id), "email": u.email, "role": u.role,
         "shop_id": u.shop_id, "is_active": u.is_active} for u in users
    ]}


# ── FEATURE 11: Cash Flow Extension ──────────────────────────────────────────

@router.get("/cashflow")
async def cashflow(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    query = select(Order)
    if current_user.role == "shop_admin":
        query = query.where(Order.shop_id == current_user.shop_id)
    elif shop_id:
        query = query.where(Order.shop_id == shop_id)

    result = await db.execute(query)
    orders = result.scalars().all()

    total = sum(o.grand_total or 0 for o in orders)
    completed = sum(o.grand_total or 0 for o in orders if o.status in ("completed", "delivered"))
    pending = sum(o.grand_total or 0 for o in orders if o.status == "pending")

    return {
        "total_revenue": total,
        "completed_revenue": completed,
        "pending_revenue": pending,
        "total_orders": len(orders),
        "completed_orders": len([o for o in orders if o.status in ("completed", "delivered")]),
        "transactions": [
            {"order_id": str(o.id), "order_number": o.order_number,
             "amount": o.grand_total, "status": o.status, "shop_id": o.shop_id}
            for o in orders
        ]
    }
