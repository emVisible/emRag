from pydantic import BaseModel


class CreateOrGetTenantType(BaseModel):
    name: str
