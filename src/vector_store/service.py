import requests
from chromadb import HttpClient
from langchain_chroma import Chroma
from langchain_community.embeddings import XinferenceEmbeddings
from langchain_core.documents import Document

from src.config import chroma_addr, xinference_addr, xinference_embedding_model_id

embedding_function = XinferenceEmbeddings(
    model_uid=xinference_embedding_model_id, server_url=xinference_addr
)
http_client = HttpClient(host="127.0.0.1", port=8080)
base_url = chroma_addr


# 创建collection
def collection_create(name: str, tenant_name: str, database_name: str, metadata: dict):
    Chroma.from_documents(
        documents=[Document(f"{metadata}")],
        embedding=embedding_function,
        collection_name=name,
        client=http_client,
    )
    return "ok"


# 获取collection数量
def get_collection_names():
    return http_client.list_collections()


# 根据名称获取collection详细信息
def collection_get_detail(name: str):
    collection = http_client.get_collection(name)
    raw = collection.get()
    res = []
    name = collection.name
    documents = raw["documents"]
    ids = raw["ids"]
    metadatas = raw["metadatas"]
    for i in range(1, len(ids)):
        item = {}
        if not metadatas[i]:
            continue
        else:
            item["metadata"] = metadatas[i]["source"].split("/")[-1]
            item["id"] = ids[i]
            item["name"] = name
            if len(documents[i]) > 80:
                item["document"] = documents[i][:77] + "..."
                item["is_document_trunc"] = True
            else:
                item["document"] = documents[i]
                item["is_document_trunc"] = False
            res.append(item)
    res.sort(key=lambda item: item["metadata"] is None)
    print(res)
    return res


def get_document(collection_name: str, document_id: str):
    collection = http_client.get_collection(collection_name)
    return collection.get(document_id)


# 获取所有collection信息
def collection_get_all():
    collections = http_client.list_collections(limit=10, offset=0)
    res = []
    for i in collections:
        name = i.name
        res.append({"collection": name, **i.get()})
    return res


def collection_get_name_all():
    collections = http_client.list_collections(limit=10, offset=0)
    res = []
    for i in collections:
        res.append(i.name)
    return res


# 删除collection
def collection_delete(name: str):
    http_client.delete_collection(name=name)


# 根据document id和document, 单量更新document
def document_update(document_id: str, document: Document):
    Chroma.update_document(document_id=document_id, document=document)


# 创建database
def database_create(name: str, tenant: str):
    res = requests.post(
        f"{base_url}/databases", params={"tenant": tenant}, json={"name": name}
    )
    if res.status_code == 200:
        return "OK"


# 获取database
def database_get(name: str, tenant: str):
    res = requests.get(f"{base_url}/databases/{name}", params={"tenant": tenant})
    if res.status_code == 200:
        return res.json()


# 创建tenant
def tenant_create(name: str):
    res = requests.post(f"{base_url}/tenants", json={"name": name})
    if res.status_code == 200:
        return "OK"


# 获取tenant
def tenant_get(name: str):
    res = requests.get(f"{base_url}/tenants/{name}")
    if res.status_code == 200:
        return res.json()


# 敏感操作: 重置数据库
def reset_vector_db():
    res = requests.post(f"{base_url}/reset")
    if res.status_code == 200:
        return "OK"
