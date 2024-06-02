from fastapi import (
    status,
    HTTPException,
    Depends,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from passlib.context import CryptContext
from jose import jwt, JWTError

from datetime import datetime, timedelta
from dotenv import load_dotenv, dotenv_values


from . import schemas,models
from .database import get_db
from .service_user import get_user_by_name


ALGORITHM = dotenv_values(".env").get("ALGORITHM")
SECRET_KEY = dotenv_values(".env").get("SECRET_KEY")
# SECRET_KEY = load_dotenv("SECRET_KEY")
# token crypto context
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

def create_user(db: Session, user: schemas.UserRegistry):
    """
    创建用户 / 用户注册
    user: 传入的user为schemas中定义的UserRegistry对象, 包含其对应属性
    """
    hashed_passwd = hash_password(user.password)
    new_user = models.User(email=user.email, name=user.name, password=hashed_passwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db, username, password):
    """
    验证用户是否存在, 若存在则对密码进行校验
    校验成功则返回用户信息
    """
    user = get_user_by_name(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, get_password_hash(password)):
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


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    对token解码, 通过token解析出用户信息(用户信息在数据库中查找)
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User validation error(JWT error)",
        headers={"WWW-Authenticate": "bearer"},
    )
    try:
        payload: dict = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_data = schemas.TokenData(username=username)
        if not username:
            raise credential_exception
    except JWTError:
        raise credential_exception
    # 根据解析出的usrname, 从数据库查找用户信息
    user = get_user_by_name(db=db, username=token_data.username)
    if not user:
        raise credential_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    """
    根据token获取当前用户信息
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not active"
        )
    return current_user
