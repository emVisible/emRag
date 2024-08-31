from pydantic import BaseModel


class CreateOrGetTenantDto(BaseModel):
    name: str
