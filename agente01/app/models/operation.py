"""Operation model — represents an underwater service operation."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Operation(Base):
    __tablename__ = "operations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    cliente: Mapped[str] = mapped_column(String(255), nullable=False)
    navio: Mapped[str] = mapped_column(String(255), nullable=False)
    imo: Mapped[str] = mapped_column(String(50), nullable=True)
    local: Mapped[str] = mapped_column(String(255), nullable=True)
    porto: Mapped[str] = mapped_column(String(255), nullable=True)
    data_operacao: Mapped[datetime] = mapped_column(Date, nullable=True)
    tipo_servico: Mapped[str] = mapped_column(String(50), nullable=False)
    areas_inspecionadas: Mapped[list] = mapped_column(ARRAY(String), nullable=True)
    descricao_servico: Mapped[str] = mapped_column(Text, nullable=True)
    equipe: Mapped[dict] = mapped_column(JSONB, nullable=True)
    equipamentos: Mapped[list] = mapped_column(ARRAY(String), nullable=True)
    condicoes: Mapped[dict] = mapped_column(JSONB, nullable=True)
    observacoes_campo: Mapped[str] = mapped_column(Text, nullable=True)
    recomendacoes_iniciais: Mapped[str] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
