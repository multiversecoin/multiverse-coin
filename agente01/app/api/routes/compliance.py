"""LGPD compliance routes — incident reporting and data purge."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rbac import Role, require_roles, check_permission
from app.api.deps import get_current_user, get_client_info
from app.models.user import User
from app.models.operation import Operation
from app.models.evidence import Evidence
from app.models.report import Report
from app.schemas.audit import ComplianceEventResponse, ComplianceIncidentCreate
from app.services.audit_service import create_audit_log, create_compliance_event
from app.services.storage_service import delete_file

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.post("/incident", response_model=ComplianceEventResponse, status_code=status.HTTP_201_CREATED)
async def register_incident(
    body: ComplianceIncidentCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "register_incident"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    event = await create_compliance_event(db, "INCIDENT", body.description, current_user.id)

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "REGISTER_INCIDENT", "COMPLIANCE", str(event.id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={"description": body.description},
    )

    await db.flush()
    await db.refresh(event)
    return event


@router.post("/purge_operation/{operation_id}")
async def purge_operation(
    operation_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    require_roles([Role.ADMIN])(current_user.role)

    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    operation = result.scalar_one_or_none()
    if not operation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operação não encontrada")

    evidences_result = await db.execute(
        select(Evidence).where(Evidence.operation_id == operation_id)
    )
    evidences = evidences_result.scalars().all()
    for ev in evidences:
        try:
            delete_file(ev.storage_key)
        except Exception:
            pass

    reports_result = await db.execute(
        select(Report).where(Report.operation_id == operation_id)
    )
    reports = reports_result.scalars().all()
    for rpt in reports:
        for key in [rpt.docx_storage_key, rpt.pdf_storage_key]:
            if key:
                try:
                    delete_file(key)
                except Exception:
                    pass

    await db.execute(delete(Evidence).where(Evidence.operation_id == operation_id))
    await db.execute(delete(Report).where(Report.operation_id == operation_id))
    await db.execute(delete(Operation).where(Operation.id == operation_id))

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "PURGE_DATA", "OPERATION", str(operation_id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={
            "evidences_purged": len(evidences),
            "reports_purged": len(reports),
            "cliente": operation.cliente,
            "navio": operation.navio,
        },
    )

    await create_compliance_event(
        db, "PURGE",
        f"Operação {operation_id} expurgada por {current_user.email}. "
        f"Evidências removidas: {len(evidences)}, Relatórios removidos: {len(reports)}.",
        current_user.id,
    )

    return {
        "detail": "Operação expurgada com sucesso",
        "evidences_purged": len(evidences),
        "reports_purged": len(reports),
    }
