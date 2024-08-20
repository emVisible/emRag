from pydantic import BaseModel


class CreateCollectionType(BaseModel):
    name: str
    configuration: dict
    metadata: dict
    get_or_create: bool
