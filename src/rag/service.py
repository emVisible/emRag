from asyncio import get_running_loop

from langchain_chroma import Chroma

from src.xinference.service import embedding_function, llm_model, rerank_model

from ..config import db_addr, k
from ..prompt import system_dynamic_prompt
from .dto.rearank import RerankResultSchemas


async def rerank_loop(document: list[str], question: str):
    loop = get_running_loop()
    res: RerankResultSchemas = await loop.run_in_executor(
        None, rerank_model.rerank, document, question, None, None, True
    )
    return res


# rerank结果统一处理
async def unify_filter(data: list[dict]):
    res = []
    for part in data:
        filter_res = sorted(
            part["results"], key=lambda x: x["relevance_score"], reverse=True
        )
        shuffled_res = [
            item["document"]["text"]
            for item in filter_res
            if item["relevance_score"] > 0
        ]
        if shuffled_res:
            res.append(shuffled_res)
        else:
            continue
    if len(res) > 0:
        return res[0][0]
    return "无"


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
    res = await unify_filter(data=data)
    return res


# 动态提示词拼接
async def create_system_dynamic_prompt(question: str, context: str):
    res = llm_model.chat(
        prompt=question,
        system_prompt=system_dynamic_prompt,
        chat_history=[],
        generate_config={
            "max_tokens": 1024,
        },
    )
    prompt = res["choices"][0]["message"]["content"]
    res = f"""[需要处理的问题]:\n{question}\n[可参考的提示]:\n{prompt}\n[已知文档信息]:\n{context}"""
    return res
