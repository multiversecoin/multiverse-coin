"""Celery tasks for report generation."""

import io
import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.hashing import compute_sha256_from_bytes
from app.core.signature import sign_data
from app.models.operation import Operation
from app.models.evidence import Evidence
from app.models.report import Report
from app.models.audit import AuditLog
from app.services.report_service import generate_report_docx
from app.services.pdf_service import convert_docx_to_pdf
from app.services.storage_service import upload_file, download_file, generate_report_storage_key
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)


@celery_app.task(bind=True, name="generate_report", max_retries=2)
def generate_report_task(self, report_id: str, operation_id: str, user_id: str):
    """Generate DOCX and PDF report for an operation."""
    with Session(engine) as db:
        try:
            report = db.execute(
                select(Report).where(Report.id == uuid.UUID(report_id))
            ).scalar_one_or_none()

            if not report:
                logger.error(f"Report {report_id} not found")
                return {"status": "failed", "error": "Report not found"}

            report.status = "generating"
            db.commit()

            operation = db.execute(
                select(Operation).where(Operation.id == uuid.UUID(operation_id))
            ).scalar_one_or_none()

            if not operation:
                report.status = "failed"
                db.commit()
                return {"status": "failed", "error": "Operation not found"}

            evidences_rows = db.execute(
                select(Evidence).where(Evidence.operation_id == uuid.UUID(operation_id))
            ).scalars().all()

            op_dict = {
                "cliente": operation.cliente,
                "navio": operation.navio,
                "imo": operation.imo,
                "local": operation.local,
                "porto": operation.porto,
                "data_operacao": str(operation.data_operacao) if operation.data_operacao else None,
                "tipo_servico": operation.tipo_servico,
                "areas_inspecionadas": operation.areas_inspecionadas,
                "descricao_servico": operation.descricao_servico,
                "equipe": operation.equipe,
                "equipamentos": operation.equipamentos,
                "condicoes": operation.condicoes,
                "observacoes_campo": operation.observacoes_campo,
                "recomendacoes_iniciais": operation.recomendacoes_iniciais,
            }

            evidences_list = []
            evidence_images = {}

            for ev in evidences_rows:
                ev_dict = {
                    "id": str(ev.id),
                    "storage_key": ev.storage_key,
                    "filename_original": ev.filename_original,
                    "sha256": ev.sha256,
                    "tags": ev.tags,
                    "observacao_operador": ev.observacao_operador,
                    "uploaded_at": str(ev.uploaded_at),
                    "tipo": ev.tipo,
                }
                evidences_list.append(ev_dict)

                if ev.tipo == "FOTO":
                    try:
                        img_data = download_file(ev.storage_key)
                        evidence_images[ev.storage_key] = img_data
                    except Exception as e:
                        logger.warning(f"Could not download evidence {ev.storage_key}: {e}")

            docx_bytes = generate_report_docx(op_dict, evidences_list, evidence_images)

            try:
                pdf_bytes = convert_docx_to_pdf(docx_bytes)
            except Exception as e:
                logger.warning(f"PDF conversion failed: {e}. Saving DOCX only.")
                pdf_bytes = None

            docx_key = generate_report_storage_key(operation_id, "docx")
            upload_file(io.BytesIO(docx_bytes), docx_key, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", len(docx_bytes))

            report.docx_storage_key = docx_key
            report.docx_sha256 = compute_sha256_from_bytes(docx_bytes)

            if pdf_bytes:
                pdf_key = generate_report_storage_key(operation_id, "pdf")
                upload_file(io.BytesIO(pdf_bytes), pdf_key, "application/pdf", len(pdf_bytes))
                report.pdf_storage_key = pdf_key
                report.pdf_sha256 = compute_sha256_from_bytes(pdf_bytes)

                signature = sign_data(pdf_bytes)
                report.signature = signature

            report.status = "ready"
            db.commit()

            audit_log = AuditLog(
                user_id=uuid.UUID(user_id),
                action="GENERATE_REPORT",
                target_type="REPORT",
                target_id=report_id,
                details_json={
                    "operation_id": operation_id,
                    "docx_sha256": report.docx_sha256,
                    "pdf_sha256": report.pdf_sha256,
                },
            )
            db.add(audit_log)
            db.commit()

            return {
                "status": "ready",
                "report_id": report_id,
                "docx_sha256": report.docx_sha256,
                "pdf_sha256": report.pdf_sha256,
            }

        except Exception as exc:
            logger.exception(f"Report generation failed: {exc}")
            if report:
                report.status = "failed"
                db.commit()
            raise self.retry(exc=exc, countdown=30)
