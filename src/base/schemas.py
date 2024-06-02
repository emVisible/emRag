from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    用户基类
    """

    name: str = Field(..., min_length=1, max_length=30)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    """
    用户登录类, 继承自用户基类, 属性包含:
      name,
      email,
      password
    """

    password: str = Field(..., min_length=1, max_length=30)


class UserRegistry(UserBase):
    """
    用户注册类, 继承自用户基类, 属性包含:
      name,
      email,
      password
    """

    password: str = Field(..., min_length=1, max_length=30)


class History(BaseModel):
    """
    历史记录类, 继承自BaseModel
    """

    id: int
    owner_id: int
    content: str

    class Config:
        orm_mode = True


class User(UserBase):
    """
    用户类, 继承自用户基类, 属性包含:
      id,
      name,
      email,
      history,
    """

    id: int
    history: list[History] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    """
    Token类
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class Crawl(BaseModel):
    city: str
    amount: int
    is_multi: bool


class FinetuneConig(BaseModel):
    data_path: str
    max_samples: int


class ExportModel(BaseModel):
    dir_name: str


class Deploy(BaseModel):
    name: str


class DeployAuto(BaseModel):
    city: str
    amount: int
    max_samples: int
    dir_name: str
    is_multi: bool
