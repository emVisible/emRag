from datetime import datetime, timedelta

from os import getenv
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

ALGORITHM = getenv("ALGORITHM") or "HS256"
SECRET_KEY = getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth")


def hash_password(password: str) -> str:
    """
    密码加密
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    密码校验
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    """
    获取明文密码对应的哈希散列值
    """
    return pwd_context.hash(plain_password)


def authenticate_user(db, user):
    """
    验证用户是否存在, 若存在则对密码进行校验
    校验成功则返回用户信息
    """
    if not user:
        return False
    if not verify_password(user.password, get_password_hash(user.password)):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    创建token / 更新expire time
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt