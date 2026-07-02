"""
Alt Print - Audit Log Service
Records every admin and system action
"""
import json
import logging
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import AuditLog

logger = logging.getLogger(__name__)


async def log_action(
    db: AsyncSession,
    actor: str,
    action: str,
    target: Optional[str] = None,
    details: Optional[Any] = None,
    role: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> None:
    """
    Write an audit log entry.
    Silently fails so it never breaks the main request flow.
    """
    try:
        details_str = None
        if details is not None:
            if isinstance(details, (dict, list)):
                details_str = json.dumps(details, default=str)
            else:
                details_str = str(details)

        entry = AuditLog(
            actor=actor,
            role=role,
            action=action,
            target=target,
            details=details_str,
            ip_address=ip_address,
        )
        db.add(entry)
        await db.flush()
        logger.debug(f"Audit: {actor} -> {action} -> {target}")
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")
