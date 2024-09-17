from ..config import (
    xinference_addr,
    xinference_llm_model_id,
    xinference_rerank_model_id,
    xinference_embedding_model_id,
)
from asyncio import Lock
from xinference.client import RESTfulClient
from langchain_community.embeddings import XinferenceEmbeddings

model_lock = Lock()
client = RESTfulClient(base_url=xinference_addr or "http://127.0.0.1:9997")
llm_model = client.get_model(model_uid=xinference_llm_model_id or "qwen2-instruct")
rerank_model = client.get_model(model_uid=xinference_rerank_model_id)

embedding_function = XinferenceEmbeddings(
    server_url=xinference_addr, model_uid=xinference_embedding_model_id
)
