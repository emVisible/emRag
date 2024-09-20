from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from src.base.database import get_db
from src.base.models import Collection, Database, Tenant
from src.utils import Tags

from .document_loader import embedding_all_from_dir, embedding_document
from .dto.collection import CreateCollectionDto, GetCollectionDto
from .dto.database import CreateDatabaseDto, GetDatabaseDto
from .dto.tenant import CreateOrGetTenantDto
from .dto.document import GetDocumentDto
from .service import (
    collection_create,
    get_document,
    collection_get_detail,
    collection_get_name_all,
    get_collection_names,
    database_create,
    database_get,
    tenant_create,
    tenant_get,
)

route_vector = APIRouter(prefix="/vector_store")


@route_vector.get(
    "/collections",
    summary="[Vector Database] 返回所有collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_collections(db: Session = Depends(get_db)):
    res = []
    collections = db.query(Collection).all()
    for index, collection in enumerate(collections):
        item = {}
        item["id"] = index + 1
        item["name"] = collection.name
        item["vest_database"] = (
            db.query(Database)
            .filter(Database.id == collection.database_id)
            .first()
            .name
        )
        item["vest_tenant"] = (
            db.query(Tenant).filter(Tenant.id == collection.database_id).first().name
        )
        res.append(item)
    return res


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


@route_vector.get(
    "/collection/names",
    summary="[Vector Database] 返回collections的name列表",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_collection_names():
    return collection_get_name_all()


@route_vector.post(
    "/collection/create",
    summary="[Vector Database] 创建collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_collection(dto: CreateCollectionDto, db: Session = Depends(get_db)):
    name = dto.name
    tenant_name = dto.tenant_name
    database_name = dto.database_name
    metadata = dto.metadata
    aim_db_id = (
        db.query(Database)
        .filter(Database.tenant_name == tenant_name and Database.name == database_name)
        .first()
        .id
    )
    db.add(Collection(name=name, database_id=aim_db_id))
    db.commit()
    return collection_create(
        name=name,
        tenant_name=tenant_name,
        database_name=database_name,
        metadata=metadata,
    )


@route_vector.post(
    "/database/get",
    summary="[Vector Database] 根据名称返回database",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_database(dto: GetDatabaseDto):
    name = dto.name
    tenant = dto.tenant
    return database_get(name=name, tenant=tenant)


@route_vector.get(
    "/databases",
    summary="[Vector Database] 返回所有database",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_database(db: Session = Depends(get_db)):
    return db.query(Database).all()


@route_vector.post(
    "/database/create",
    summary="[Vector Database] 创建database",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_database(dto: CreateDatabaseDto, db: Session = Depends(get_db)):
    name = dto.name
    tenant = dto.tenant
    db.add(Database(name=name, tenant_name=tenant))
    db.commit()
    return database_create(name=name, tenant=tenant)


@route_vector.post(
    "/tenant/create",
    summary="[Vector Database] 创建tenant",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_tenant(dto: CreateOrGetTenantDto, db: Session = Depends(get_db)):
    name = dto.name
    tenant_create(name=name)
    db.add(Tenant(name=name))
    db.commit()
    return "OK"


@route_vector.get(
    "/tenants",
    summary="[Vector Database] 获取所有tenants",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_all_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()


@route_vector.post(
    "/tenant/get",
    summary="[Vector Database] 根据名称获取tenant",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def create_collection(dto: CreateOrGetTenantDto):
    name = dto.name
    return tenant_get(name=name)


@route_vector.post(
    "/upload_single/{collection_name}",
    summary="[RAG] 根据单一文档转换为矢量",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def upload_single(collection_name: str, file: UploadFile = File(...)):
    return embedding_document(collection_name=collection_name, file=file)


@route_vector.post(
    "/generate",
    summary="[RAG] 批量创建矢量库",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def generate():
    embedding_all_from_dir()


@route_vector.get(
    "/collections/get_detail_all",
    summary="[Vector Database] 返回collections detail",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.dev],
)
async def collections_detail_all():
    names = await get_collection_names()
    print(names)
    res = []
    for name in names:
        part = collection_get_detail(name)
        res.append(part)
    return res


@route_vector.post(
    "/collections/get_document",
    summary="[Vector Database] 返回collections detail",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.dev],
)
async def document_detail_get(dto: GetDocumentDto):
    collection_name = dto.collection_name
    document_id = dto.document_id
    res = get_document(collection_name=collection_name, document_id=document_id)
    return res["documents"][0]
