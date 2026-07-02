"""
Alt Print - Feature Flags Endpoints
Dynamic feature toggle without backend restart
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_client_ip, get_current_user, require_role
from app.db.database import get_db
from app.models.models import FeatureFlag, User
from app.schemas.schemas import APIResponse, FeatureFlagOut, ToggleFeatureRequest
from app.services.audit import log_action
from app.services.cache import cache_get, cache_set, invalidate_feature_cache
from app.services.websocket import broadcast_feature_flag_update

router = APIRouter(prefix="/features", tags=["Feature Flags"])

CACHE_TTL = 60  # 60 seconds cache for feature flags


@router.get("", response_model=List[FeatureFlagOut])
async def get_features(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all feature flags.
    - Without shop_id: returns global flags
    - With shop_id: returns shop-specific overrides merged with globals
    """
    cache_key = f"altprint:features:{'shop:' + shop_id if shop_id else 'global'}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    if shop_id:
        # Fetch global flags + shop overrides
        result = await db.execute(
            select(FeatureFlag).where(
                (FeatureFlag.scope == "global") |
                ((FeatureFlag.scope == "shop") & (FeatureFlag.shop_id == shop_id))
            )
        )
        flags = result.scalars().all()

        # Merge: shop overrides take precedence
        merged: dict = {}
        for flag in flags:
            if flag.scope == "global":
                if flag.feature_name not in merged:
                    merged[flag.feature_name] = flag
            else:
                merged[flag.feature_name] = flag  # shop override wins

        result_flags = list(merged.values())
    else:
        result = await db.execute(
            select(FeatureFlag).where(FeatureFlag.scope == "global")
        )
        result_flags = result.scalars().all()

    data = [FeatureFlagOut.model_validate(f) for f in result_flags]
    await cache_set(cache_key, [f.model_dump() for f in data], ttl=CACHE_TTL)
    return data


@router.post("/toggle", response_model=APIResponse)
async def toggle_feature(
    body: ToggleFeatureRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Toggle a feature flag.
    - Super admin: can toggle global or any shop flag
    - Shop admin: can only toggle their own shop's flags
    """
    # Authorization
    if current_user.role == "shop_admin":
        if body.shop_id != current_user.shop_id:
            raise HTTPException(status_code=403, detail="Can only modify your own shop's features")
    elif current_user.role not in ("super_admin",):
        raise HTTPException(status_code=403, detail="Not authorized to modify feature flags")

    scope = "shop" if body.shop_id else "global"

    # Find or create the flag
    query = select(FeatureFlag).where(
        and_(
            FeatureFlag.feature_name == body.feature_name,
            FeatureFlag.scope == scope,
            FeatureFlag.shop_id == body.shop_id,
        )
    )
    result = await db.execute(query)
    flag = result.scalar_one_or_none()

    if flag:
        flag.enabled = body.enabled
        flag.updated_by = str(current_user.email or current_user.phone)
    else:
        # Create shop-specific override
        flag = FeatureFlag(
            feature_name=body.feature_name,
            label=body.feature_name.replace("_", " ").title(),
            enabled=body.enabled,
            scope=scope,
            shop_id=body.shop_id,
            updated_by=str(current_user.email or current_user.phone),
        )
        db.add(flag)

    await db.flush()
    await db.refresh(flag)

    # Invalidate cache
    await invalidate_feature_cache(body.shop_id)

    # Broadcast via WebSocket
    await broadcast_feature_flag_update(
        {
            "feature_name": flag.feature_name,
            "label": flag.label,
            "enabled": flag.enabled,
            "scope": flag.scope,
            "shop_id": flag.shop_id,
        },
        shop_id=body.shop_id,
    )

    # Audit log
    action = "ENABLE_FEATURE" if body.enabled else "DISABLE_FEATURE"
    await log_action(
        db,
        actor=str(current_user.email or current_user.phone),
        action=action,
        target=body.feature_name,
        details={"shop_id": body.shop_id, "enabled": body.enabled},
        role=current_user.role,
        ip_address=get_client_ip(request),
    )

    return APIResponse(
        message=f"Feature '{body.feature_name}' {'enabled' if body.enabled else 'disabled'}",
        data=FeatureFlagOut.model_validate(flag),
    )


@router.post("/enable", response_model=APIResponse)
async def enable_feature(
    feature_name: str,
    shop_id: Optional[str] = None,
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Enable a feature flag"""
    return await toggle_feature(
        ToggleFeatureRequest(feature_name=feature_name, enabled=True, shop_id=shop_id),
        request, db, current_user
    )


@router.post("/disable", response_model=APIResponse)
async def disable_feature(
    feature_name: str,
    shop_id: Optional[str] = None,
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Disable a feature flag"""
    return await toggle_feature(
        ToggleFeatureRequest(feature_name=feature_name, enabled=False, shop_id=shop_id),
        request, db, current_user
    )
