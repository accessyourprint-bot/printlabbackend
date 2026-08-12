import io

path = "app/api/v1/endpoints/delivery.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_imports = """from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import DeliveryPerson, User
from app.schemas.schemas import APIResponse, DeliveryPersonCreate, DeliveryPersonOut, DeliveryPersonUpdate"""

new_imports = """from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import DeliveryPerson, Order, User
from app.schemas.schemas import APIResponse, DeliveryPersonCreate, DeliveryPersonOut, DeliveryPersonUpdate, DeliveryPersonWithCountOut"""

c1 = content.count(old_imports)
print(f"Imports anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_imports, new_imports)
    print("Imports updated")
else:
    print("WARNING: imports anchor not found")

old_route = """@router.post("", response_model=APIResponse, status_code=201)
async def create_delivery_person("""

new_route = """@router.get("/with-order-counts", response_model=List[DeliveryPersonWithCountOut])
async def list_delivery_persons_with_counts(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("super_admin", "shop_admin")),
):
    \"\"\"List delivery persons along with how many orders each has been assigned.\"\"\"
    query = select(DeliveryPerson)
    if current_user.role == "shop_admin":
        query = query.where(DeliveryPerson.shop_id == current_user.shop_id)
    elif shop_id:
        query = query.where(DeliveryPerson.shop_id == shop_id)
    result = await db.execute(query.order_by(DeliveryPerson.name))
    persons = result.scalars().all()

    count_result = await db.execute(
        select(Order.delivery_person_id, func.count(Order.id))
        .where(Order.delivery_person_id.isnot(None))
        .group_by(Order.delivery_person_id)
    )
    counts = dict(count_result.all())

    out = []
    for p in persons:
        item = DeliveryPersonWithCountOut.model_validate(p)
        item.order_count = counts.get(p.id, 0)
        out.append(item)
    return out


@router.post("", response_model=APIResponse, status_code=201)
async def create_delivery_person("""

c2 = content.count(old_route)
print(f"Route anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_route, new_route)
    print("with-order-counts endpoint added")
else:
    print("WARNING: route anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
