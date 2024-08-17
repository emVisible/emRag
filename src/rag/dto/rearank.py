from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class Document(BaseModel):
    text: str


class Result(BaseModel):
    index: int
    relevance_score: float
    document: Document


class Meta(BaseModel):
    api_version: Optional[str] = None
    billed_units: Optional[int] = None
    tokens: Optional[int] = None
    warnings: Optional[str] = None


class RerankResultSchemas(BaseModel):
    id: UUID
    results: List[Result]
    meta: Meta
