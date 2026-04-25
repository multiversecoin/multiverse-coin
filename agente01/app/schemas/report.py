"""Report schemas."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: uuid.UUID
    operation_id: uuid.UUID
    status: str
    docx_sha256: Optional[str]
    pdf_sha256: Optional[str]
    signature: Optional[str]
    signed_by: Optional[uuid.UUID]
    signed_at: Optional[datetime]
    created_by: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportVerifyResponse(BaseModel):
    report_id: uuid.UUID
    docx_integrity: bool
    pdf_integrity: bool
    signature_valid: bool
    signed_by: Optional[uuid.UUID]
    signed_at: Optional[datetime]


class ReportGenerateResponse(BaseModel):
    report_id: uuid.UUID
    task_id: str
    status: str
    message: str
