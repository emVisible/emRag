from pydantic import BaseModel
from typing import Dict


class GetCollectionDto(BaseModel):
    name: str


class CreateCollectionDto(BaseModel):
    name: str
    tenant_name: str
    database_name: str
    metadata: Dict[str, str]
