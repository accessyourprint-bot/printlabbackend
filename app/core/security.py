"""
Alt Print - Security Utilities
JWT tokens, password hashing, AES-256 encryption, token management
"""
import base64
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT Tokens ---
def create_access_token(
    subject: Union[str, Any],
    role: str,
    extra_data: Optional[Dict] = None,
) -> str:
    """Create a JWT access token"""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(subject),
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
        "jti": secrets.token_urlsafe(16),
    }
    if extra_data:
        payload.update(extra_data)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: Union[str, Any], role: str) -> str:
    """Create a JWT refresh token"""
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": str(subject),
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": secrets.token_urlsafe(16),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Dict:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")


# --- AES-256-GCM Encryption ---
def _get_aes_key() -> bytes:
    """Derive a 32-byte AES key from the configured key"""
    key_str = settings.AES_ENCRYPTION_KEY
    # Use SHA-256 to get exactly 32 bytes
    return hashlib.sha256(key_str.encode()).digest()


def encrypt_file(data: bytes) -> tuple[bytes, bytes]:
    """
    Encrypt file data using AES-256-GCM.
    Returns: (encrypted_data, nonce)
    The nonce must be stored alongside the encrypted data for decryption.
    """
    key = _get_aes_key()
    nonce = os.urandom(12)  # 96-bit nonce for GCM
    aesgcm = AESGCM(key)
    encrypted = aesgcm.encrypt(nonce, data, None)
    return encrypted, nonce


def decrypt_file(encrypted_data: bytes, nonce: bytes) -> bytes:
    """Decrypt file data using AES-256-GCM"""
    key = _get_aes_key()
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, encrypted_data, None)


def generate_secure_filename(original_filename: str) -> str:
    """
    Generate a cryptographically secure random filename.
    Original filename is never used in storage.
    """
    ext = ""
    if "." in original_filename:
        ext = "." + original_filename.rsplit(".", 1)[1].lower()
    return secrets.token_hex(32) + ext


def generate_otp() -> str:
    """Generate a 4-digit OTP"""
    return str(secrets.randbelow(9000) + 1000)
