"""
Alt Print - Redis Cache Service
Caching, feature flag lookups, OTP storage, rate limiting
"""
import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import settings

_redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


# ============================================================
# GENERIC CACHE OPERATIONS
# ============================================================
async def cache_set(key: str, value: Any, ttl: int = None) -> None:
    redis = await get_redis()
    ttl = ttl or settings.REDIS_CACHE_TTL
    await redis.setex(key, ttl, json.dumps(value, default=str))


async def cache_get(key: str) -> Optional[Any]:
    redis = await get_redis()
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None


async def cache_delete(key: str) -> None:
    redis = await get_redis()
    await redis.delete(key)


async def cache_delete_pattern(pattern: str) -> None:
    redis = await get_redis()
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)


# ============================================================
# FEATURE FLAG CACHE
# ============================================================
FEATURE_FLAG_KEY = "altprint:features:global"
SHOP_FEATURE_KEY = "altprint:features:shop:{shop_id}"
SYSTEM_CONFIG_KEY = "altprint:system:config"


async def invalidate_feature_cache(shop_id: Optional[str] = None) -> None:
    """Invalidate feature flag cache (global or shop-specific)"""
    if shop_id:
        await cache_delete(SHOP_FEATURE_KEY.format(shop_id=shop_id))
    else:
        await cache_delete(FEATURE_FLAG_KEY)
        await cache_delete_pattern("altprint:features:shop:*")


async def invalidate_system_config_cache() -> None:
    """Invalidate system config cache"""
    await cache_delete(SYSTEM_CONFIG_KEY)


# ============================================================
# OTP STORAGE
# ============================================================
OTP_KEY = "altprint:otp:{phone}"
OTP_TTL = 300  # 5 minutes


async def store_otp(phone: str, otp: str) -> None:
    redis = await get_redis()
    await redis.setex(OTP_KEY.format(phone=phone), OTP_TTL, otp)


async def verify_otp(phone: str, otp: str) -> bool:
    redis = await get_redis()
    stored = await redis.get(OTP_KEY.format(phone=phone))
    if stored and stored == otp:
        await redis.delete(OTP_KEY.format(phone=phone))
        return True
    return False


# ============================================================
# RATE LIMITING
# ============================================================
async def check_rate_limit(key: str, limit: int, window: int = 60) -> tuple[bool, int]:
    """
    Check if rate limit is exceeded.
    Returns (is_allowed, remaining_requests)
    """
    redis = await get_redis()
    rate_key = f"altprint:ratelimit:{key}"
    pipe = redis.pipeline()
    pipe.incr(rate_key)
    pipe.expire(rate_key, window)
    results = await pipe.execute()
    count = results[0]
    allowed = count <= limit
    remaining = max(0, limit - count)
    return allowed, remaining


# ============================================================
# BRUTE FORCE PROTECTION
# ============================================================
async def record_failed_login(identifier: str) -> int:
    """Record a failed login attempt, return total failures"""
    redis = await get_redis()
    key = f"altprint:login_fail:{identifier}"
    count = await redis.incr(key)
    await redis.expire(key, 900)  # 15 minutes window
    return count


async def clear_failed_login(identifier: str) -> None:
    redis = await get_redis()
    await redis.delete(f"altprint:login_fail:{identifier}")


async def get_failed_logins(identifier: str) -> int:
    redis = await get_redis()
    val = await redis.get(f"altprint:login_fail:{identifier}")
    return int(val) if val else 0


# ============================================================
# WEBSOCKET PRESENCE
# ============================================================
WS_CLIENTS_KEY = "altprint:ws:clients"


async def register_ws_client(client_id: str, user_id: Optional[str], role: str) -> None:
    redis = await get_redis()
    data = json.dumps({"user_id": user_id, "role": role})
    await redis.hset(WS_CLIENTS_KEY, client_id, data)
    await redis.expire(WS_CLIENTS_KEY, 86400)


async def deregister_ws_client(client_id: str) -> None:
    redis = await get_redis()
    await redis.hdel(WS_CLIENTS_KEY, client_id)


async def get_ws_client_count() -> int:
    redis = await get_redis()
    return await redis.hlen(WS_CLIENTS_KEY)
