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

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
