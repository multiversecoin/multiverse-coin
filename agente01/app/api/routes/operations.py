"""Operation CRUD routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rbac import check_permission
from app.api.deps import get_current_user, get_client_info
from app.models.user import User
from app.models.operation import Operation
from app.schemas.operation import OperationCreate, OperationResponse, OperationUpdate
from app.services.audit_service import create_audit_log

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.post("", response_model=OperationResponse, status_code=status.HTTP_201_CREATED)
async def create_operation(
    body: OperationCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "create_operation"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    op = Operation(
        cliente=body.cliente,
        navio=body.navio,
        imo=body.imo,
        local=body.local,
        porto=body.porto,
        data_operacao=body.data_operacao,
        tipo_servico=body.tipo_servico,
        areas_inspecionadas=body.areas_inspecionadas,
        descricao_servico=body.descricao_servico,
        equipe=[m.model_dump() for m in body.equipe] if body.equipe else None,
        equipamentos=body.equipamentos,
        condicoes=body.condicoes.model_dump() if body.condicoes else None,
        observacoes_campo=body.observacoes_campo,
        recomendacoes_iniciais=body.recomendacoes_iniciais,
        created_by=current_user.id,
    )
    db.add(op)
    await db.flush()
    await db.refresh(op)

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "CREATE_OPERATION", "OPERATION", str(op.id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
    )

    return op


@router.get("", response_model=list[OperationResponse])
async def list_operations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "read_operation"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(select(Operation).order_by(Operation.created_at.desc()))
    return result.scalars().all()


@router.get("/{operation_id}", response_model=OperationResponse)
async def get_operation(
    operation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "read_operation"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    op = result.scalar_one_or_none()
    if not op:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operação não encontrada")
    return op


@router.patch("/{operation_id}", response_model=OperationResponse)
async def update_operation(
    operation_id: uuid.UUID,
    body: OperationUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not check_permission(current_user.role, "update_operation"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")

    result = await db.execute(select(Operation).where(Operation.id == operation_id))
    op = result.scalar_one_or_none()
    if not op:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operação não encontrada")

    update_data = body.model_dump(exclude_unset=True)
    if "equipe" in update_data and update_data["equipe"] is not None:
        update_data["equipe"] = [m.model_dump() if hasattr(m, "model_dump") else m for m in update_data["equipe"]]
    if "condicoes" in update_data and update_data["condicoes"] is not None:
        cond = update_data["condicoes"]
        update_data["condicoes"] = cond.model_dump() if hasattr(cond, "model_dump") else cond

    for key, value in update_data.items():
        setattr(op, key, value)

    await db.flush()
    await db.refresh(op)

    client_info = get_client_info(request)
    await create_audit_log(
        db, current_user.id, "UPDATE_OPERATION", "OPERATION", str(op.id),
        ip_address=client_info["ip_address"],
        user_agent=client_info["user_agent"],
        details={"updated_fields": list(update_data.keys())},
    )

    return op
