"""Audit and compliance schemas."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    action: str
    target_type: Optional[str]
    target_id: Optional[str]
    ip_address: Optional[str]
    timestamp: datetime
    details_json: Optional[dict]

    model_config = {"from_attributes": True}


class ComplianceIncidentCreate(BaseModel):
    description: str


class ComplianceEventResponse(BaseModel):
    id: uuid.UUID
    type: str
    description: str
    created_by: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
