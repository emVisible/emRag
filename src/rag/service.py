from langchain_chroma import Chroma
from langchain_community.embeddings import XinferenceEmbeddings
from xinference.client import Client
from os import getenv

from .dto.rearank import RerankResultSchemas
from ..utils import log
from ..config import (
    xinference_addr,
    xinference_embedding_model_id,
    xinference_rerank_model_id,
    db_addr,
    k,
)

# 加载配置
client = Client(base_url=xinference_addr)
rerank_model = client.get_model(xinference_rerank_model_id)


# rag文档检索, 通过文本转换为向量, 通过向量检索以及rerank返回合适结果
@log("RAG搜索中... (1/2)")
def similarity_search(question: str) -> str:
    embedding_function = XinferenceEmbeddings(
        server_url=xinference_addr, model_uid=xinference_embedding_model_id
    )
    db = Chroma(persist_directory=db_addr, embedding_function=embedding_function)
    question = f"{question or '介绍一下杭州'}"
    context = db.similarity_search(query=question, k=k)
    documents = []
    for chunk in context:
        print(f"chunk元数据: {chunk.metadata}")
        documents.append(chunk.page_content)
    res: RerankResultSchemas = rerank_model.rerank(
        documents=documents, query=question, return_documents=True
    )
    shuffled_res = sorted(
        res["results"], key=lambda x: x["relevance_score"], reverse=True
    )[:3]
    return shuffled_res


# 根据检索结果生成一个Context, 构建提问词
@log("提问词生成中... (2/2)")
def create_prompt(question: str, context: str) -> str:
    prompt_template = f"""
    [问题]:
      {question}
    [已知信息]:
      {context}
    """
    return prompt_template


# 清空对话, 清空向量数据库中的对话相关数据
@log("向量库清除中...")
def gc() -> None:
    vector_db = Chroma(persist_directory=db_addr)
    vector_db.delete_collection()
    print("[System] GC回收完毕")
