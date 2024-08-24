from fastapi import APIRouter, HTTPException, status

from src.utils import Tags

from .dto.collection import GetCollectionType
from .service import (
    collection_create,
    collection_update,
    collection_get_all,
    collection_get_detail,
)

route_vector = APIRouter(prefix="/vector_store")


@route_vector.get(
    "/collections",
    summary="[Vector Database] 返回所有collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_collections():
    return collection_get_all()


@route_vector.post(
    "/collection/get",
    summary="[Vector Database] 根据名称返回collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_collection(dto: GetCollectionType):
    name = dto.name
    return collection_get_detail(name)


@route_vector.post(
    "/collection/create",
    summary="[Vector Database] 根据名称返回collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_collection():
    collection_create()
    return "OK"
