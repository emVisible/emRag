from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=4, max_length=256)


class UserSchemas(UserBase):
    role_id: int = Field(...)


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchemas(BaseModel):
    username: str
