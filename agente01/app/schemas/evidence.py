"""Evidence schemas."""

import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class EvidenceResponse(BaseModel):
    id: uuid.UUID
    operation_id: uuid.UUID
    filename_original: str
    file_size: int
    sha256: str
    content_type: Optional[str]
    tipo: str
    tags: Optional[List[str]]
    observacao_operador: Optional[str]
    uploaded_by: uuid.UUID
    uploaded_at: datetime

    model_config = {"from_attributes": True}
