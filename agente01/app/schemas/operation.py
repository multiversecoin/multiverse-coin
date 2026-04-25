"""Operation schemas."""

import uuid
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel


class TeamMember(BaseModel):
    nome: str
    funcao: str
    certificacao: Optional[str] = None


class OperationalConditions(BaseModel):
    visibilidade: Optional[str] = None
    correnteza: Optional[str] = None
    mare: Optional[str] = None
    observacoes: Optional[str] = None


class OperationCreate(BaseModel):
    cliente: str
    navio: str
    imo: Optional[str] = None
    local: Optional[str] = None
    porto: Optional[str] = None
    data_operacao: Optional[date] = None
    tipo_servico: str
    areas_inspecionadas: Optional[List[str]] = None
    descricao_servico: Optional[str] = None
    equipe: Optional[List[TeamMember]] = None
    equipamentos: Optional[List[str]] = None
    condicoes: Optional[OperationalConditions] = None
    observacoes_campo: Optional[str] = None
    recomendacoes_iniciais: Optional[str] = None


class OperationUpdate(BaseModel):
    cliente: Optional[str] = None
    navio: Optional[str] = None
    imo: Optional[str] = None
    local: Optional[str] = None
    porto: Optional[str] = None
    data_operacao: Optional[date] = None
    tipo_servico: Optional[str] = None
    areas_inspecionadas: Optional[List[str]] = None
    descricao_servico: Optional[str] = None
    equipe: Optional[List[TeamMember]] = None
    equipamentos: Optional[List[str]] = None
    condicoes: Optional[OperationalConditions] = None
    observacoes_campo: Optional[str] = None
    recomendacoes_iniciais: Optional[str] = None


class OperationResponse(BaseModel):
    id: uuid.UUID
    cliente: str
    navio: str
    imo: Optional[str]
    local: Optional[str]
    porto: Optional[str]
    data_operacao: Optional[date]
    tipo_servico: str
    areas_inspecionadas: Optional[List[str]]
    descricao_servico: Optional[str]
    equipe: Optional[list]
    equipamentos: Optional[List[str]]
    condicoes: Optional[dict]
    observacoes_campo: Optional[str]
    recomendacoes_iniciais: Optional[str]
    created_by: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
