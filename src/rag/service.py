from asyncio import get_running_loop

from langchain_chroma import Chroma

from src.xinference.service import embedding_function, llm_model, rerank_model


from logging import getLogger
from ..config import db_addr, k, min_relevance_score
from .dto.rearank import RerankResultSchemas

logger = getLogger(__name__)


async def rerank_loop(document: list[str], question: str):
    loop = get_running_loop()
    res: RerankResultSchemas = await loop.run_in_executor(
        None, rerank_model.rerank, document, question, None, None, True
    )
    return res


# rerank结果统一处理
async def unify_filter(data: list[dict], question: str):
    res = []
    log_msg = []
    for part in data:
        filter_res = sorted(
            part["results"], key=lambda x: x["relevance_score"], reverse=True
        )
        shuffled_res = [
            item["document"]["text"]
            for item in filter_res
            if item["relevance_score"] > min_relevance_score
        ]
        log_msg.append(
            [
                {
                    "doc": item["document"]["text"][:30] + "...",
                    "score": item["relevance_score"],
                }
                for item in filter_res
                if item["relevance_score"] > min_relevance_score
            ]
        )
        if shuffled_res:
            res.append(shuffled_res)
        else:
            continue
    logger.info(f"=========问题: {question}============")
    logger.info(log_msg)
    logger.info(f"====================================")
    if len(res) > 0:
        return res[0][0]
    return False


# 分块rerank
async def batch_rerank(question: str, sourece_document: list[str]):
    reranked_data = []
    for document in sourece_document:
        part_res = await rerank_loop(document=[document], question=question)
        reranked_data.append(part_res)
    return reranked_data


# rag文档检索, 通过文本转换为向量, 通过向量检索以及rerank返回合适结果
async def similarity_search(question: str, collection_name: str) -> str:
    db = Chroma(
        persist_directory=db_addr,
        embedding_function=embedding_function,
        collection_name=collection_name,
    )
    context = db.similarity_search(query=question, k=k)
    documents = [item.page_content for item in context]
    rerank_loop(document=documents, question=question)
    data = await batch_rerank(question=question, sourece_document=documents)
    res = await unify_filter(data=data, question=question)
    return res


# 静态提示词拼接
async def create_system_static_prompt(question: str, context: str):
    return f"[需要处理的问题]:\n{question}\n[已知文档信息]:\n{context or '(无参考信息, 请按提示要求返回)'}"


# 动态提示词拼接
# async def create_system_dynamic_prompt(question: str, context: str):
#     res = llm_model.chat(
#         prompt=question,
#         system_prompt=system_dynamic_prompt,
#         chat_history=[],
#         generate_config={
#             "max_tokens": 1024,
#         },
#     )
#     prompt = res["choices"][0]["message"]["content"]
#     res = f"""[需要处理的问题]:\n{question}\n[可参考的提示]:\n{prompt}\n[已知文档信息]:\n{context}"""
#     return res