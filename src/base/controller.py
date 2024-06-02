from fastapi import status, HTTPException, Depends, APIRouter
from enum import Enum
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import timedelta
from dotenv import dotenv_values

from . import schemas, service_user
from .database import get_db
from .service_auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    create_user
)

route_base = APIRouter(prefix="/base")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    dotenv_values(".env").get("ACCESS_TOKEN_EXPIRE_MINUTES")
)


class Tags(Enum):
    user = "User"
    util = "Util"
    token = "Token"
    history = "History"
    auth = "Auth"


@route_base.post(
    "/registry",
    summary="创建用户",
    response_model=schemas.User,
    response_description="返回创建的用户信息",
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.user],
)
def create_user_route(user: schemas.UserRegistry, db: Session = Depends(get_db)):
    db_user = service_user.get_user_by_email(db=db, user_email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="该邮箱已注册"
        )
    return create_user(db=db, user=user)


@route_base.get(
    "/user/{user_id}",
    summary="根据id获取指定用户",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User,
    response_description="返回指定用户信息",
    tags=[Tags.user],
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = service_user.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户未注册")
    return user


@route_base.get(
    "/users",
    summary="获取所有用户",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.User],
    response_description="返回用户组成的list",
    tags=[Tags.user],
)
def get_user_all(offset=0, limit=100, db: Session = Depends(get_db)):
    users = service_user.get_users(db=db, offset=offset, limit=limit)
    return users


@route_base.post(
    "/user/{user_id}/history",
    summary="为指定用户创建history信息",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.History,
    response_description="返回创建的历史信息",
    tags=[Tags.history],
)
def create_user_history(
    user_id: int, history: schemas.History, db: Session = Depends(get_db)
):
    return service_user.create_history(db=db, history=history, user_id=user_id)


@route_base.get(
    "/history",
    summary="[仅限开发] 获取全部历史记录",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.History],
    response_description="返回所有历史记录(可限制条数)",
    tags=[Tags.history],
)
def get_history_all(limit=40, db: Session = Depends(get_db)):
    return service_user.get_history_all(db=db, limit=limit)


@route_base.post(
    "/auth",
    summary="为登录用户设置token",
    status_code=status.HTTP_200_OK,
    response_description="返回token信息",
    tags=[Tags.auth],
)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@route_base.get(
    "/current",
    summary="获取当前用户",
    status_code=status.HTTP_200_OK,
    response_description="返回当前用户的信息",
    response_model=schemas.User,
    tags=[Tags.auth],
)
async def check_current_user(
    user: schemas.User = Depends(get_current_active_user),
):
    print(user.name)
    return user