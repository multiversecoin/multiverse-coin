"""Audit logging service — all actions are recorded."""

import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog, ComplianceEvent


async def create_audit_log(
    db: AsyncSession,
    user_id: Optional[uuid.UUID],
    action: str,
    target_type: Optional[str] = None,
    target_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[dict] = None,
) -> AuditLog:
    log = AuditLog(
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=str(target_id) if target_id else None,
        ip_address=ip_address,
        user_agent=user_agent,
        details_json=details,
    )
    db.add(log)
    await db.flush()
    return log


async def create_compliance_event(
    db: AsyncSession,
    event_type: str,
    description: str,
    created_by: uuid.UUID,
) -> ComplianceEvent:
    event = ComplianceEvent(
        type=event_type,
        description=description,
        created_by=created_by,
    )
    db.add(event)
    await db.flush()
    return event
