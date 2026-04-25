"""Report model — generated DOCX/PDF with digital signature."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    operation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("operations.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending | generating | ready | approved | failed
    docx_storage_key: Mapped[str] = mapped_column(String(500), nullable=True)
    pdf_storage_key: Mapped[str] = mapped_column(String(500), nullable=True)
    docx_sha256: Mapped[str] = mapped_column(String(64), nullable=True)
    pdf_sha256: Mapped[str] = mapped_column(String(64), nullable=True)
    signature: Mapped[str] = mapped_column(Text, nullable=True)
    signed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
