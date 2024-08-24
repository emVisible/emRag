from fastapi import APIRouter, Depends, HTTPException, status
from langchain.embeddings import XinferenceEmbeddings
from langchain_chroma import Chroma
from chromadb import HttpClient, AdminClient, AsyncHttpClient
from langchain_core.documents import Document
from typing import List

from src.config import (
    db_addr,
    xinference_addr,
    xinference_embedding_model_id,
)

embedding_function = XinferenceEmbeddings(
    model_uid=xinference_embedding_model_id, server_url=xinference_addr
)

admin_client = AdminClient()
persistent_client = HttpClient(host="127.0.0.1", port=8080)


# 创建collection
def collection_create(collection_name: str, documents: List[Document]):
    Chroma.from_documents(
        collection_name=collection_name,
        documents=documents,
        embedding=embedding_function,
        persist_directory=db_addr,
    )


# 获取collection数量
def collection_get_count():
    return persistent_client.count_collections()


# 根据名称获取collection详细信息
def collection_get_detail(name: str):
    collection = persistent_client.get_collection(name)
    res = collection.get()
    res["collection"] = collection.name
    return res


# 获取所有collection信息
def collection_get_all():
    collections = persistent_client.list_collections(limit=10, offset=0)
    res = []
    for i in collections:
        name = i.name
        res.append({"collection": name, **i.get()})
    return res


# 删除collection
def collection_delete(name: str):
    persistent_client.delete_collection(name=name)


# 根据document id和document, 单量更新document
def document_update(document_id: str, document: Document):
    Chroma.update_document(document_id=document_id, document=document)


# 创建database
def database_create(name: str, tenant: str):
    admin_client.create_database(name=name, tenant=tenant)


# 获取database
def database_get(name: str, tenant: str):
    admin_client.get_database(name=name, tenant=tenant)


# 创建tenant
def tenant_create(name: str):
    admin_client.create_tenant(name=name)


# 获取tenant
def tenant_get(name: str):
    admin_client.get_tenant(name=name)


# 敏感操作: 重置数据库
def reset():
    persistent_client.reset()