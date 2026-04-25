"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="OPERADOR"),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("cliente", sa.String(255), nullable=False),
        sa.Column("navio", sa.String(255), nullable=False),
        sa.Column("imo", sa.String(50)),
        sa.Column("local", sa.String(255)),
        sa.Column("porto", sa.String(255)),
        sa.Column("data_operacao", sa.Date),
        sa.Column("tipo_servico", sa.String(50), nullable=False),
        sa.Column("areas_inspecionadas", postgresql.ARRAY(sa.String)),
        sa.Column("descricao_servico", sa.Text),
        sa.Column("equipe", postgresql.JSONB),
        sa.Column("equipamentos", postgresql.ARRAY(sa.String)),
        sa.Column("condicoes", postgresql.JSONB),
        sa.Column("observacoes_campo", sa.Text),
        sa.Column("recomendacoes_iniciais", sa.Text),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "evidences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("operation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("operations.id"), nullable=False, index=True),
        sa.Column("storage_key", sa.String(500), nullable=False),
        sa.Column("filename_original", sa.String(255), nullable=False),
        sa.Column("file_size", sa.BigInteger, nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False, index=True),
        sa.Column("content_type", sa.String(100)),
        sa.Column("tipo", sa.String(10), nullable=False, server_default="FOTO"),
        sa.Column("tags", postgresql.ARRAY(sa.String)),
        sa.Column("observacao_operador", sa.Text),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("previous_version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("evidences.id")),
    )

    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("operation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("operations.id"), nullable=False, index=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("docx_storage_key", sa.String(500)),
        sa.Column("pdf_storage_key", sa.String(500)),
        sa.Column("docx_sha256", sa.String(64)),
        sa.Column("pdf_sha256", sa.String(64)),
        sa.Column("signature", sa.Text),
        sa.Column("signed_by", postgresql.UUID(as_uuid=True)),
        sa.Column("signed_at", sa.DateTime(timezone=True)),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True)),
        sa.Column("action", sa.String(50), nullable=False, index=True),
        sa.Column("target_type", sa.String(50)),
        sa.Column("target_id", sa.String(100)),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.String(500)),
        sa.Column("details_json", postgresql.JSONB),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
    )

    op.create_table(
        "compliance_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("compliance_events")
    op.drop_table("audit_logs")
    op.drop_table("reports")
    op.drop_table("evidences")
    op.drop_table("operations")
    op.drop_table("users")
