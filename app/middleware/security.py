"""
Alt Print - Security Middleware
Rate limiting, secure headers, request validation
"""
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.services.cache import check_rate_limit


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Global rate limiting middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks and docs
        if request.url.path in ("/health", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)

        # Get client IP
        forwarded_for = request.headers.get("X-Forwarded-For")
        ip = forwarded_for.split(",")[0].strip() if forwarded_for else (
            request.client.host if request.client else "unknown"
        )

        # Stricter limit for auth endpoints
        if "/auth/login" in request.url.path or "/auth/otp" in request.url.path:
            limit = settings.LOGIN_RATE_LIMIT_PER_MINUTE
        else:
            limit = settings.RATE_LIMIT_PER_MINUTE

        allowed, remaining = await check_rate_limit(f"global:{ip}", limit)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please slow down."},
                headers={"Retry-After": "60"},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        if not settings.DEBUG:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        # Remove server header
        if "server" in response.headers: del response.headers["server"]

        return response


class MaintenanceMiddleware(BaseHTTPMiddleware):
    """Block requests when maintenance mode or emergency lock is active"""

    EXEMPT_PATHS = {"/health", "/api/v1/system/config", "/api/v1/auth/login",
                   "/docs", "/openapi.json", "/redoc", "/ws"}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip exempt paths
        path = request.url.path
        if any(path.startswith(p) or path == p for p in self.EXEMPT_PATHS):
            return await call_next(request)

        # Check system config from cache/DB only on API requests
        if path.startswith("/api/"):
            try:
                from app.services.cache import cache_get, SYSTEM_CONFIG_KEY
                config = await cache_get(SYSTEM_CONFIG_KEY)

                if config:
                    if config.get("emergency_lock"):
                        return JSONResponse(
                            status_code=503,
                            content={
                                "detail": "Platform is temporarily locked. Please try again later.",
                                "code": "EMERGENCY_LOCK",
                            },
                        )
                    if not config.get("app_enabled", True):
                        return JSONResponse(
                            status_code=503,
                            content={
                                "detail": "Platform is currently offline.",
                                "code": "APP_DISABLED",
                            },
                        )
                    if config.get("maintenance_mode"):
                        return JSONResponse(
                            status_code=503,
                            content={
                                "detail": "Platform is under maintenance. Please try again soon.",
                                "code": "MAINTENANCE",
                            },
                        )
            except Exception:
                pass  # Don't block if cache check fails

        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log request timing and basic info"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)

        # Add timing header
        response.headers["X-Response-Time"] = f"{duration_ms}ms"
        return response

