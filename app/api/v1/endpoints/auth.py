"""
Alt Print - Authentication Endpoints
Register, Login (email+password / phone+OTP), Refresh, Logout
"""
import hashlib
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_client_ip, get_current_user
from app.core.config import settings
from app.services.sms import send_otp_sms
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_otp,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.models.models import RefreshToken, SystemConfig, User
from app.schemas.schemas import (
    APIResponse,
    LoginRequest,
    OTPRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserOut,
)
from app.services.audit import log_action
from app.services.cache import (
    cache_get,
    check_rate_limit,
    clear_failed_login,
    get_failed_logins,
    record_failed_login,
    store_otp,
    verify_otp,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

MAX_FAILED_LOGINS = 5


async def _check_login_guard(db: AsyncSession) -> None:
    """Ensure login is globally enabled"""
    result = await db.execute(select(SystemConfig).where(SystemConfig.id == 1))
    config = result.scalar_one_or_none()
    if config and (not config.login_enabled or config.emergency_lock):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Login is currently disabled",
        )


@router.post("/register", response_model=APIResponse)
async def register(
    body: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user account"""
    await _check_login_guard(db)

    if not body.email and not body.phone:
        raise HTTPException(status_code=400, detail="Email or phone required")

    # Check for duplicates
    if body.email:
        existing = await db.execute(select(User).where(User.email == body.email))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already registered")

    if body.phone:
        existing = await db.execute(select(User).where(User.phone == body.phone))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Phone already registered")

    user = User(
        email=body.email,
        phone=body.phone,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
        role="user",
        is_active=True,
    )
    db.add(user)
    await db.flush()

    await log_action(
        db, body.email or body.phone, "REGISTER", str(user.id),
        role="user", ip_address=get_client_ip(request)
    )

    return APIResponse(message="Registration successful", data={"user_id": str(user.id)})


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Login with email+password or phone+OTP"""
    await _check_login_guard(db)

    ip = get_client_ip(request)
    identifier = body.email or body.phone or ip

    # Rate limit check
    allowed, remaining = await check_rate_limit(
        f"login:{ip}", settings.LOGIN_RATE_LIMIT_PER_MINUTE
    )
    if not allowed:
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again later.")

    # Find user
    user = None
    if body.email:
        result = await db.execute(select(User).where(User.email == body.email))
        user = result.scalar_one_or_none()
    elif body.phone:
        result = await db.execute(select(User).where(User.phone == body.phone))
        user = result.scalar_one_or_none()

    if not user:
        await record_failed_login(identifier)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check account lockout
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=423, detail="Account temporarily locked due to failed attempts")

    # Validate credentials
    if body.password:
        if not user.hashed_password or not verify_password(body.password, user.hashed_password):
            fails = await record_failed_login(identifier)
            if fails >= MAX_FAILED_LOGINS:
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
                await db.flush()
            raise HTTPException(status_code=401, detail="Invalid credentials")

    elif body.otp:
        if not body.phone or not await verify_otp(body.phone, body.otp):
            await record_failed_login(identifier)
            raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    else:
        raise HTTPException(status_code=400, detail="Password or OTP required")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")

    # Clear failure counter on success
    await clear_failed_login(identifier)
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.now(timezone.utc)

    # Issue tokens
    extra = {}
    if user.shop_id:
        extra["shop_id"] = user.shop_id

    access_token = create_access_token(str(user.id), user.role, extra)
    refresh_token = create_refresh_token(str(user.id), user.role)

    # Store refresh token hash
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    rt = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        device_info=request.headers.get("User-Agent", "")[:500],
        ip_address=ip,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(rt)
    await db.flush()

    await log_action(db, str(user.email or user.phone), "LOGIN", str(user.id),
                     role=user.role, ip_address=ip)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        role=user.role,
        user_id=str(user.id),
    )


@router.post("/otp/send", response_model=APIResponse)
async def send_otp(
    body: OTPRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Send OTP to phone number"""
    await _check_login_guard(db)

    ip = get_client_ip(request)
    allowed, _ = await check_rate_limit(f"otp:{ip}", 5)
    if not allowed:
        raise HTTPException(status_code=429, detail="Too many OTP requests")

    otp = generate_otp()
    await store_otp(body.phone, otp)

    # Send OTP via Fast2SMS
    phone_clean = body.phone.strip().replace(" ", "").replace("-", "").replace("+91", "").replace("+", "")
    await send_otp_sms(phone_clean, otp)

    return APIResponse(message="OTP sent successfully")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """Exchange a refresh token for new tokens"""
    try:
        payload = decode_token(body.refresh_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    token_hash = hashlib.sha256(body.refresh_token.encode()).hexdigest()
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked == False,
        )
    )
    stored_token = result.scalar_one_or_none()

    if not stored_token or stored_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")

    # Revoke old token (rotation)
    stored_token.is_revoked = True

    user_result = await db.execute(select(User).where(User.id == stored_token.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or disabled")

    extra = {}
    if user.shop_id:
        extra["shop_id"] = user.shop_id

    new_access = create_access_token(str(user.id), user.role, extra)
    new_refresh = create_refresh_token(str(user.id), user.role)

    new_hash = hashlib.sha256(new_refresh.encode()).hexdigest()
    new_rt = RefreshToken(
        user_id=user.id,
        token_hash=new_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(new_rt)
    await db.flush()

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        role=user.role,
        user_id=str(user.id),
    )


@router.post("/logout", response_model=APIResponse)
async def logout(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """Revoke refresh token on logout"""
    try:
        token_hash = hashlib.sha256(body.refresh_token.encode()).hexdigest()
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        token = result.scalar_one_or_none()
        if token:
            token.is_revoked = True
            await db.flush()
    except Exception:
        pass
    return APIResponse(message="Logged out successfully")


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user




