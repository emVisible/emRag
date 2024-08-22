from uuid import uuid4
from fastapi import Depends, APIRouter, status
from langchain.embeddings import XinferenceEmbeddings
from langchain_chroma import Chroma
from chromadb.api import ClientAPI

from langchain_core.documents import Document
import httpx
import requests
from src.config import chroma_addr
from fastapi import HTTPException
from .dto.collection import CreateCollectionType
from json import dumps, dump

from src.config import xinference_addr, xinference_embedding_model_id
from .database import get_client
from src.utils import Tags
from .service import create_collection
from .dto.collection import CreateCollectionType

route_vector = APIRouter(prefix="/vector_store")

@route_vector.get(
    "/collections",
    summary="[Vector Database] 返回所有collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_collections(
    client: ClientAPI = Depends(get_client),
):
    return client.list_collections()


@route_vector.post(
    "/collection",
    summary="[Vector Database] 根据名称返回collection",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.vector_db],
)
async def get_collection_by_name(name: str, client: ClientAPI = Depends(get_client)):
    return client.get_collection(name=name)
