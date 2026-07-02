"""
Alt Print - Storage Service
AES-256-GCM encrypted file upload/download via AWS S3 or Cloudflare R2
"""
import logging
from pathlib import Path
from typing import Optional, Tuple

import aioboto3
from botocore.exceptions import ClientError

from app.core.config import settings
from app.core.security import decrypt_file, encrypt_file, generate_secure_filename

logger = logging.getLogger(__name__)


def _local_storage_root() -> Path:
    root = Path(settings.LOCAL_STORAGE_PATH).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _local_storage_file(storage_key: str) -> Path:
    root = _local_storage_root()
    path = (root / storage_key).resolve()
    if root not in path.parents:
        raise RuntimeError("Invalid storage key")
    return path


def _get_s3_config() -> dict:
    """Build boto3 session config based on storage provider"""
    if settings.STORAGE_PROVIDER == "r2":
        return {
            "aws_access_key_id": settings.R2_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.R2_SECRET_ACCESS_KEY,
            "endpoint_url": settings.R2_ENDPOINT_URL,
            "region_name": "auto",
        }
    return {
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        "region_name": settings.AWS_REGION,
    }


def _get_bucket() -> str:
    if settings.STORAGE_PROVIDER == "r2":
        return settings.R2_BUCKET
    return settings.AWS_S3_BUCKET


async def upload_encrypted_file(
    file_data: bytes,
    original_filename: str,
    content_type: str,
) -> Tuple[str, str]:
    """
    Encrypt and upload a file to S3/R2.
    Returns: (storage_key, nonce_hex)
    - storage_key: random key used in the bucket (never original name)
    - nonce_hex: hex-encoded nonce needed for decryption
    """
    encrypted_data, nonce = encrypt_file(file_data)
    storage_key = generate_secure_filename(original_filename)
    nonce_hex = nonce.hex()

    if settings.STORAGE_PROVIDER == "local":
        path = _local_storage_file(storage_key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(encrypted_data)
        logger.info("Uploaded encrypted file to local storage: %s", storage_key)
        return storage_key, nonce_hex

    bucket = _get_bucket()

    session = aioboto3.Session()
    async with session.client("s3", **_get_s3_config()) as s3:
        try:
            await s3.put_object(
                Bucket=bucket,
                Key=storage_key,
                Body=encrypted_data,
                ContentType="application/octet-stream",  # Obscure content type
                Metadata={
                    "encrypted": "aes-256-gcm",
                    "nonce": nonce_hex,
                    # Never store original filename in metadata
                },
                ServerSideEncryption="AES256",  # S3-level encryption on top
            )
            logger.info(f"Uploaded encrypted file: {storage_key}")
            return storage_key, nonce_hex
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            raise RuntimeError(f"Storage upload failed: {str(e)}")


async def download_decrypted_file(storage_key: str, nonce_hex: str) -> bytes:
    """
    Download and decrypt a file from S3/R2.
    Returns the decrypted file bytes.
    """
    nonce = bytes.fromhex(nonce_hex)

    if settings.STORAGE_PROVIDER == "local":
        path = _local_storage_file(storage_key)
        if not path.is_file():
            raise RuntimeError("Stored file not found")
        return decrypt_file(path.read_bytes(), nonce)

    bucket = _get_bucket()

    session = aioboto3.Session()
    async with session.client("s3", **_get_s3_config()) as s3:
        try:
            response = await s3.get_object(Bucket=bucket, Key=storage_key)
            encrypted_data = await response["Body"].read()
            return decrypt_file(encrypted_data, nonce)
        except ClientError as e:
            logger.error(f"S3 download failed: {e}")
            raise RuntimeError(f"Storage download failed: {str(e)}")


async def delete_file_from_storage(storage_key: str) -> bool:
    """
    Permanently delete a file from S3/R2.
    This is irreversible.
    """
    if settings.STORAGE_PROVIDER == "local":
        path = _local_storage_file(storage_key)
        try:
            path.unlink(missing_ok=True)
            logger.info("Permanently deleted local file: %s", storage_key)
            return True
        except OSError as e:
            logger.error("Local delete failed for %s: %s", storage_key, e)
            return False

    bucket = _get_bucket()
    session = aioboto3.Session()
    async with session.client("s3", **_get_s3_config()) as s3:
        try:
            await s3.delete_object(Bucket=bucket, Key=storage_key)
            logger.info(f"Permanently deleted: {storage_key}")
            return True
        except ClientError as e:
            logger.error(f"S3 delete failed for {storage_key}: {e}")
            return False


async def check_storage_connection() -> bool:
    """Health check for storage connection"""
    if settings.STORAGE_PROVIDER == "local":
        try:
            _local_storage_root()
            return True
        except OSError:
            return False

    bucket = _get_bucket()
    session = aioboto3.Session()
    async with session.client("s3", **_get_s3_config()) as s3:
        try:
            await s3.head_bucket(Bucket=bucket)
            return True
        except Exception:
            return False
