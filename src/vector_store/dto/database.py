from pydantic import BaseModel


class GetDatabaseDto(BaseModel):
    name: str
    tenant: str

class CreateDatabaseDto(BaseModel):
    name: str
    tenant: str