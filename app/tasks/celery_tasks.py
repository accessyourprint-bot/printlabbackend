"""
Alt Print - Celery Background Tasks
Auto-delete expired files, cleanup jobs
"""
import asyncio
import logging
from datetime import datetime, timezone

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create Celery app
celery_app = Celery(
    "altprint",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    "delete-expired-files": {
        "task": "app.tasks.celery_tasks.delete_expired_files",
        "schedule": crontab(minute=0, hour="*/6"),  # Every 6 hours
    },
    "cleanup-revoked-tokens": {
        "task": "app.tasks.celery_tasks.cleanup_revoked_tokens",
        "schedule": crontab(minute=0, hour=2),  # Daily at 2 AM
    },
    "cleanup-old-audit-logs": {
        "task": "app.tasks.celery_tasks.cleanup_old_audit_logs",
        "schedule": crontab(minute=0, hour=3, day_of_week=0),  # Weekly
    },
}


@celery_app.task(name="app.tasks.celery_tasks.delete_expired_files", bind=True, max_retries=3)
def delete_expired_files(self):
    """
    Delete all uploaded files that have exceeded the 7-day retention period.
    This is IRREVERSIBLE. Files are deleted from both S3/R2 and the database.
    """
    asyncio.run(_async_delete_expired_files())


async def _async_delete_expired_files():
    """Async implementation of expired file deletion"""
    from sqlalchemy import select, update
    from app.db.database import AsyncSessionLocal
    from app.models.models import OrderFile
    from app.services.storage import delete_file_from_storage

    now = datetime.now(timezone.utc)
    deleted_count = 0
    failed_count = 0

    async with AsyncSessionLocal() as db:
        # Find all expired files not yet deleted
        result = await db.execute(
            select(OrderFile).where(
                OrderFile.expires_at <= now,
                OrderFile.deleted_at == None,
                OrderFile.status != "deleted",
            )
        )
        expired_files = result.scalars().all()

        for f in expired_files:
            try:
                # Delete from S3/R2 first
                storage_deleted = await delete_file_from_storage(f.storage_key)

                if storage_deleted:
                    # Wipe all sensitive metadata
                    f.storage_key = "DELETED"
                    f.nonce = "DELETED"
                    f.original_filename = "DELETED"
                    f.status = "deleted"
                    f.deleted_at = now
                    deleted_count += 1
                    logger.info(f"Deleted expired file: {f.id}")
                else:
                    failed_count += 1
                    logger.warning(f"Failed to delete storage object for file: {f.id}")

            except Exception as e:
                failed_count += 1
                logger.error(f"Error deleting file {f.id}: {e}")

        await db.commit()
        logger.info(f"Auto-delete complete: {deleted_count} deleted, {failed_count} failed")

    return {"deleted": deleted_count, "failed": failed_count}


@celery_app.task(name="app.tasks.celery_tasks.cleanup_revoked_tokens")
def cleanup_revoked_tokens():
    """Remove expired/revoked refresh tokens from database"""
    asyncio.run(_async_cleanup_tokens())


async def _async_cleanup_tokens():
    from sqlalchemy import delete
    from app.db.database import AsyncSessionLocal
    from app.models.models import RefreshToken

    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            delete(RefreshToken).where(
                (RefreshToken.expires_at < now) | (RefreshToken.is_revoked == True)
            )
        )
        await db.commit()
        logger.info(f"Cleaned up {result.rowcount} expired/revoked tokens")


@celery_app.task(name="app.tasks.celery_tasks.cleanup_old_audit_logs")
def cleanup_old_audit_logs():
    """Remove audit logs older than 90 days"""
    asyncio.run(_async_cleanup_audit_logs())


async def _async_cleanup_audit_logs():
    from datetime import timedelta
    from sqlalchemy import delete
    from app.db.database import AsyncSessionLocal
    from app.models.models import AuditLog

    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            delete(AuditLog).where(AuditLog.created_at < cutoff)
        )
        await db.commit()
        logger.info(f"Cleaned up {result.rowcount} old audit log entries")
