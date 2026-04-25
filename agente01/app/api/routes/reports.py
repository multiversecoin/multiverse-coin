"""Report generation, download, approval, and verification routes."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.hashing import compute_sha256_from_bytes
from app.core.rbac import check_permission, Role, require_roles
from app.core.signature import sign_data, verify_signature
from app.api.deps import get_current_user, get_client_info
from app.models.user import User
from app.models.operation import Operation
from app.models.report import Report
from app.schemas.report import ReportGenerateResponse, ReportResponse, ReportVerifyResponse
from app.services.audit_service import create_audit_log
from app.services.storage_service import download_file

router = APIRouter(tags=["Reports"])


@router.post(
    "/operations/{operation_id}/report/generate",
    response_model=ReportGenerateResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_report(
    operation_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "generate_report"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operação não encontrada")

    report = Report(
        operation_id=operation_id,
        status="pending",
        created_by=current_user.id,
    )
    db.add(report)
    await db.flush()
    await db.refresh(report)

    from app.workers.tasks import generate_report_task
    task = generate_report_task.delay(
        str(report.id), str(operation_id), str(current_user.id)
    )

    return ReportGenerateResponse(
        report_id=report.id,
        task_id=task.id,
        status="pending",
        message="Relatório em geração. Use GET /operations/{id}/report/download para baixar quando pronto.",
    )


@router.post("/operations/{operation_id}/report/approve")
async def approve_report(
    operation_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    require_roles([Role.ADMIN, Role.SUPERVISOR])(current_user.role)

    result = await db.execute(
        select(Report)
        .where(Report.operation_id == operation_id, Report.status == "ready")
        .order_by(Report.created_at.desc())
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório pronto não encontrado para esta operação",
        )

    if report.pdf_storage_key:
        pdf_data = download_file(report.pdf_storage_key)
        computed_hash = compute_sha256_from_bytes(pdf_data)
        if computed_hash != report.pdf_sha256:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Integridade do PDF comprometida. Hash não confere.",
            )
        signature = sign_data(pdf_data)
        report.signature = signature
    elif report.docx_storage_key:
        docx_data = download_file(report.docx_storage_key)
        signature = sign_data(docx_data)
        report.signature = signature

    report.status = "approved"
    report.signed_by = current_user.id
    report.signed_at = datetime.now(timezone.utc)
    await db.flush()

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "APPROVE_REPORT", "REPORT", str(report.id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={"operation_id": str(operation_id)},
    )

    return {"detail": "Relatório aprovado e assinado com sucesso", "report_id": str(report.id)}


@router.get("/operations/{operation_id}/report/download")
async def download_report(
    operation_id: uuid.UUID,
    request: Request,
    format: str = Query(default="pdf", pattern="^(docx|pdf)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "download_report"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(
        select(Report)
        .where(Report.operation_id == operation_id, Report.status.in_(["ready", "approved"]))
        .order_by(Report.created_at.desc())
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relatório não encontrado ou ainda em geração",
        )

    if format == "pdf" and report.pdf_storage_key:
        data = download_file(report.pdf_storage_key)
        media_type = "application/pdf"
        filename = f"relatorio_{operation_id}.pdf"
    elif report.docx_storage_key:
        data = download_file(report.docx_storage_key)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"relatorio_{operation_id}.docx"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Formato {format} não disponível para este relatório",
        )

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "DOWNLOAD_REPORT", "REPORT", str(report.id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={"format": format},
    )

    return Response(
        content=data,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get(
    "/operations/{operation_id}/report/verify",
    response_model=ReportVerifyResponse,
)
async def verify_report(
    operation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Report)
        .where(Report.operation_id == operation_id)
        .order_by(Report.created_at.desc())
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relatório não encontrado")

    docx_ok = False
    pdf_ok = False
    sig_ok = False

    if report.docx_storage_key and report.docx_sha256:
        try:
            docx_data = download_file(report.docx_storage_key)
            docx_ok = compute_sha256_from_bytes(docx_data) == report.docx_sha256
        except Exception:
            docx_ok = False

    if report.pdf_storage_key and report.pdf_sha256:
        try:
            pdf_data = download_file(report.pdf_storage_key)
            pdf_ok = compute_sha256_from_bytes(pdf_data) == report.pdf_sha256
        except Exception:
            pdf_ok = False

    if report.signature and report.pdf_storage_key:
        try:
            pdf_data = download_file(report.pdf_storage_key)
            sig_ok = verify_signature(pdf_data, report.signature)
        except Exception:
            sig_ok = False

    return ReportVerifyResponse(
        report_id=report.id,
        docx_integrity=docx_ok,
        pdf_integrity=pdf_ok,
        signature_valid=sig_ok,
        signed_by=report.signed_by,
        signed_at=report.signed_at,
    )
