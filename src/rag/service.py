from asyncio import get_running_loop

from langchain_chroma import Chroma
from langchain_community.embeddings import XinferenceEmbeddings

from src.xinference.service import rerank_model

from ..config import db_addr, k, xinference_addr, xinference_embedding_model_id
from .dto.rearank import RerankResultSchemas


# rag文档检索, 通过文本转换为向量, 通过向量检索以及rerank返回合适结果
async def similarity_search(question: str, collection_name: str) -> str:
    embedding_function = XinferenceEmbeddings(
        server_url=xinference_addr, model_uid=xinference_embedding_model_id
    )
    db = Chroma(
        persist_directory=db_addr,
        embedding_function=embedding_function,
        collection_name=collection_name,
    )
    question = f"{question or '介绍一下杭州'}"
    context = db.similarity_search(query=question, k=k)
    documents = []
    for chunk in context:
        documents.append(chunk.page_content)
    loop = get_running_loop()
    res: RerankResultSchemas = await loop.run_in_executor(
        None, rerank_model.rerank, documents, question, None, None, True
    )
    filter_res = sorted(
        res["results"], key=lambda x: x["relevance_score"], reverse=True
    )[:3]
    shuffled_res = [item for item in filter_res if item["relevance_score"] > 0]
    return shuffled_res


# 根据检索结果生成一个Context, 构建提问词
async def create_prompt(question: str, context: str) -> str:
    prompt_template = f"""
    [问题]:
      {question}
    [已知信息]:
      {context}
    """
    return prompt_template
