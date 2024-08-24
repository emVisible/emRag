from pydantic import BaseModel


class GetCollectionType(BaseModel):
    name: str