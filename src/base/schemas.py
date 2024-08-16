from pydantic import BaseModel, EmailStr, Field


class UserSchemas(BaseModel):
    """
    用户基类
    """

    name: str = Field(..., min_length=1, max_length=30)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=4, max_length=256)
    role_id: int = Field(...)


class TokenSchemas(BaseModel):
    """
    Token类
    """

    access_token: str
    token_type: str


class TokenDataSchemas(BaseModel):
    username: str
