from fastapi import APIRouter


from fastapi import status, Depends
from src.utils import Tags
from src.base.database import get_db, reset_db
from src.vector_store.service import reset_vector_db
from sqlalchemy.orm import Session
from .db import init_traditional_db
from .vector_db import init_vector_db

route_init = APIRouter(prefix="/init")


@route_init.post(
    "/init_table",
    summary="[初始化] 初始化数据库",
    status_code=status.HTTP_200_OK,
    response_description="返回是否成功",
    tags=[Tags.init],
)
async def init_table_user(
    db: Session = Depends(get_db),
):
    reset_db()
    reset_vector_db()
    print("重置成功")
    await init_traditional_db(db=db)
    await init_vector_db(db=db)
    return "初始化成功"