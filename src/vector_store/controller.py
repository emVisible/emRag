from uuid import uuid4
from fastapi import Depends, APIRouter
from langchain.embeddings import XinferenceEmbeddings
from langchain_chroma import Chroma
from chromadb.api import ClientAPI

from langchain_core.documents import Document

from src.config import xinference_addr, xinference_embedding_model_id
from .database import get_client

route_vector = APIRouter(prefix="/vector_store")


@route_vector.post("/add")
async def add_to_vector_store(client: ClientAPI = Depends(get_client)):
    collection = client.get_or_create_collection("collection_name", metadata=)
    collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])
    embedding_function = XinferenceEmbeddings(
        server_url=xinference_addr, model_uid=xinference_embedding_model_id
    )

    vector_store_from_client = Chroma(
        client=client,
        collection_name="collection_name",
        embedding_function=embedding_function,
    )

    document_1 = Document(
        page_content="I had chocalate chip pancakes and scrambled eggs for breakfast this morning.",
        metadata={"source": "tweet"},
        id=1,
    )

    document_2 = Document(
        page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
        metadata={"source": "news"},
        id=2,
    )

    documents = [document_1, document_2]
    uuids = [str(uuid4()) for _ in range(len(documents))]

    vector_store_from_client.add_documents(documents=documents, ids=uuids)
    return "OK"
