from fastapi import APIRouter


from fastapi import status, Depends
from src.utils import Tags
from src.base.database import get_db
from sqlalchemy.orm import Session
from .db import db_init

route_init = APIRouter(prefix="/init")


@route_init.post(
    "/init_table",
    summary="初始化传统数据库表",
    status_code=status.HTTP_200_OK,
    response_description="返回是否成功",
    tags=[Tags.init],
)
async def init_table_user(
    db: Session = Depends(get_db),
):
    await db_init(db=db)
    return "初始化成功"
