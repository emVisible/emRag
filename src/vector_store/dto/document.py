from pydantic import BaseModel


class GetDocumentDto(BaseModel):
    document_id: str
    collection_name: str
