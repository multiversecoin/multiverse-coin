"""Evidence upload and management routes."""

import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.hashing import compute_sha256
from app.core.rbac import check_permission
from app.api.deps import get_current_user, get_client_info
from app.models.user import User
from app.models.operation import Operation
from app.models.evidence import Evidence
from app.schemas.evidence import EvidenceResponse
from app.services.audit_service import create_audit_log
from app.services.storage_service import upload_file, generate_storage_key, download_file

router = APIRouter(tags=["Evidences"])

ALLOWED_EXTENSIONS = set(
    settings.ALLOWED_IMAGE_EXTENSIONS.split(",") + settings.ALLOWED_VIDEO_EXTENSIONS.split(",")
)
IMAGE_EXTENSIONS = set(settings.ALLOWED_IMAGE_EXTENSIONS.split(","))
MAX_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

BLOCKED_EXTENSIONS = {".exe", ".bat", ".cmd", ".sh", ".ps1", ".msi", ".dll", ".com", ".scr"}


def _get_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename.lower())
    return ext


def _sanitize_filename(filename: str) -> str:
    safe = "".join(c for c in filename if c.isalnum() or c in "._- ")
    return safe[:200]


@router.post(
    "/operations/{operation_id}/evidences/upload",
    response_model=EvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_evidence(
    operation_id: uuid.UUID,
    request: Request,
    file: UploadFile = File(...),
    tags: str = Form(default=""),
    observacao_operador: str = Form(default=""),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "upload_evidence"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operação não encontrada")

    ext = _get_extension(file.filename or "unknown.bin")
    if ext in BLOCKED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de arquivo bloqueado")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão não permitida: {ext}. Permitidas: {ALLOWED_EXTENSIONS}",
        )

    file_data = await file.read()
    if len(file_data) > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo excede o limite de {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    import io
    file_obj = io.BytesIO(file_data)
    sha256 = compute_sha256(file_obj)

    existing = await db.execute(
        select(Evidence).where(
            Evidence.operation_id == operation_id,
            Evidence.sha256 == sha256,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Evidência duplicada (SHA256: {sha256}). Arquivo já registrado nesta operação.",
        )

    tipo = "FOTO" if ext in IMAGE_EXTENSIONS else "VIDEO"
    tag_list = [t.strip().upper() for t in tags.split(",") if t.strip()] if tags else []
    safe_name = _sanitize_filename(file.filename or "unknown")
    storage_key = generate_storage_key(str(operation_id), safe_name)
    content_type = file.content_type or "application/octet-stream"

    file_obj.seek(0)
    upload_file(file_obj, storage_key, content_type, len(file_data))

    evidence = Evidence(
        operation_id=operation_id,
        storage_key=storage_key,
        filename_original=safe_name,
        file_size=len(file_data),
        sha256=sha256,
        content_type=content_type,
        tipo=tipo,
        tags=tag_list,
        observacao_operador=observacao_operador if observacao_operador else None,
        uploaded_by=current_user.id,
    )
    db.add(evidence)
    await db.flush()
    await db.refresh(evidence)

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "UPLOAD_EVIDENCE", "EVIDENCE", str(evidence.id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={"sha256": sha256, "filename": safe_name, "operation_id": str(operation_id)},
    )

    return evidence


@router.get(
    "/operations/{operation_id}/evidences",
    response_model=list[EvidenceResponse],
)
async def list_evidences(
    operation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "read_evidence"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(
        select(Evidence)
        .where(Evidence.operation_id == operation_id)
        .order_by(Evidence.uploaded_at)
    )
    return result.scalars().all()


@router.get("/evidences/{evidence_id}/download")
async def download_evidence(
    evidence_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "download_evidence"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(select(Evidence).where(Evidence.id == evidence_id))
    evidence = result.scalar_one_or_none()
    if not evidence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidência não encontrada")

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "DOWNLOAD_EVIDENCE", "EVIDENCE", str(evidence.id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
    )

    from fastapi.responses import Response
    data = download_file(evidence.storage_key)
    return Response(
        content=data,
        media_type=evidence.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{evidence.filename_original}"'},
    )
