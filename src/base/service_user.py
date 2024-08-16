from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas
from .schemas import UserSchemas, TokenSchemas, TokenDataSchemas
from .models import User
from .auth.service_auth import SECRET_KEY, ALGORITHM, hash_password, oauth2_scheme
from .database import get_db


def create_user(db: Session, user: UserSchemas):
    hashed_passwd = hash_password(user.password)
    new_user = User(
        email=user.email,
        name=user.name,
        password=hashed_passwd,
        role_id=user.role_id or 1,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_user_by_account(db: Session, username: str, password: str):
    return (
        db.query(models.User)
        .filter(
            models.User.email == username
            and models.User.password == hash_password(password)
        )
        .first()
    )


def get_users(db: Session, offset: int | None, limit: int | None):
    return db.query(models.User).offset(offset=offset).limit(limit=limit).all()


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
        token_data = schemas.TokenDataSchemas(username=username)
        if not username:
            raise credential_exception
    except JWTError:
        raise credential_exception
    # 根据解析出的usrname, 从数据库查找用户信息
    user = get_user_by_name(db=db, username=token_data.username)
    if not user:
        raise credential_exception
    return user