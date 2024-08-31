from fastapi import APIRouter, HTTPException, status

from src.utils import Tags

from .dto.collection import GetCollectionDto, CreateCollectionDto
from .dto.tenant import CreateOrGetTenantDto
from .dto.database import GetDatabaseDto, CreateDatabaseDto
from .service import (
    collection_create,
    collection_get_all,
    collection_get_detail,
    tenant_create,
    tenant_get,
    database_create,
    database_get,
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
async def get_collection(dto: GetCollectionDto):
    name = dto.name
    return collection_get_detail(name)


@route_vector.post(
    "/collection/create",
    summary="[Vector Database] 创建collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_collection(dto: CreateCollectionDto):
    name = dto.name
    tenant_name = dto.tenant_name
    database_name = dto.database_name
    metadata = dto.metadata
    return collection_create(name=name, tenant_name=tenant_name, database_name=database_name, metadata=metadata)


@route_vector.post(
    "/database/get",
    summary="[Vector Database] 根据名称返回collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_database(dto: GetDatabaseDto):
    name = dto.name
    tenant = dto.tenant
    return database_get(name=name, tenant=tenant)


@route_vector.post(
    "/database/create",
    summary="[Vector Database] 根据名称返回collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_database(dto: CreateDatabaseDto):
    name = dto.name
    tenant = dto.tenant
    return database_create(name=name, tenant=tenant)


@route_vector.post(
    "/tenant/create",
    summary="[Vector Database] 创建tenant",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_tenant(dto: CreateOrGetTenantDto):
    name = dto.name
    tenant_create(name=name)
    return "OK"


@route_vector.post(
    "/tenant/get",
    summary="[Vector Database] 获取tenant",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_collection(dto: CreateOrGetTenantDto):
    name = dto.name
    return tenant_get(name=name)
