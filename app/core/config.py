"""
Alt Print - Core Configuration
Loads and validates all environment variables using Pydantic Settings
"""
import secrets
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator, AnyUrl
from functools import lru_cache


class Settings(BaseSettings):
    # --- Application ---
    APP_NAME: str = "AltPrint"
    APP_ENV: str = "production"
    DEBUG: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://altprint:altprint_secure_password@localhost:5433/altprint_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 300

    # --- JWT ---
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # --- Storage ---
    STORAGE_PROVIDER: str = "local"  # "local", "s3", or "r2"
    LOCAL_STORAGE_PATH: str = ".local_storage"

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "ap-south-1"
    AWS_S3_BUCKET: str = "altprint-files"

    # Cloudflare R2
    R2_ACCESS_KEY_ID: Optional[str] = None
    R2_SECRET_ACCESS_KEY: Optional[str] = None
    R2_ENDPOINT_URL: Optional[str] = None
    R2_BUCKET: str = "altprint-files"

    # --- Encryption ---
    AES_ENCRYPTION_KEY: str = secrets.token_urlsafe(32)

    # --- Payment ---
    FAST2SMS_API_KEY: str = ""
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None

    # --- Google Maps ---
    GOOGLE_MAPS_API_KEY: Optional[str] = None

    # --- Celery ---
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # --- File Settings ---
    MAX_FILE_SIZE_MB: int = 50
    FILE_RETENTION_DAYS: int = 7
    ALLOWED_EXTENSIONS: str = "pdf,docx,doc,png,jpg,jpeg"

    # --- Super Admin ---
    SUPER_ADMIN_EMAIL: str = "admin@altprint.in"
    SUPER_ADMIN_PASSWORD: str = "AltPrint2024!"

    # --- Rate Limiting ---
    RATE_LIMIT_PER_MINUTE: int = 3000
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 100

    @property
    def allowed_origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [e.strip().lower() for e in self.ALLOWED_EXTENSIONS.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()





