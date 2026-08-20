path = r"app\api\v1\endpoints\delivery.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

old = """from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import DeliveryPerson, Order, User
from app.schemas.schemas import APIResponse, DeliveryPersonCreate, DeliveryPersonOut, DeliveryPersonUpdate, DeliveryPersonWithCountOut"""

new = """from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.database import get_db
from app.models.models import DeliveryPerson, Order, User
from app.schemas.schemas import APIResponse, DeliveryPersonCreate, DeliveryPersonOut, DeliveryPersonUpdate, DeliveryPersonWithCountOut
from app.services.storage import upload_encrypted_file, download_decrypted_file

RIDER_DOC_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
RIDER_DOC_MAX_BYTES = 10 * 1024 * 1024  # 10MB"""

if src.count(old) != 1:
    raise SystemExit(f"FAILED: found {src.count(old)} matches for import block, expected 1.")

src = src.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: delivery.py imports updated.")
