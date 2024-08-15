from langchain_chroma import Chroma
from langchain_community.embeddings import XinferenceEmbeddings
from os import getenv

from ..utils import log
from .config import RAGConfig

# 加载配置
db_addr = getenv("DB_ADDR")
query_quantity = RAGConfig.QUERY_QUANTITY
xinference_embedding_model_id = getenv("XINFERENCE_EMBEDDING_MODEL_ID") or "bge-large-zh-v1.5"
xinference_addr = getenv("XINFERENCE_ADDR") or "http://127.0.0.1:9997"
print(xinference_embedding_model_id)
print(xinference_addr)


# rag文档检索, 通过文本转换为向量, 通过向量检索生成结果
@log("RAG搜索中... (1/2)")
async def similarity_search(question: str) -> str:
    embedding_function = XinferenceEmbeddings(
        server_url=xinference_addr, model_uid=xinference_embedding_model_id
    )
    db = Chroma(persist_directory=db_addr, embedding_function=embedding_function)
    question = f"{question or '介绍一下杭州'}"
    context = db.similarity_search(query=question, k=query_quantity)
    res = ""
    for chunk in context:
        print(f"chunk元数据: {chunk.metadata}")
        res += chunk.page_content
    res = res.replace("\n", "")
    return res


# 根据检索结果生成一个Context, 构建提问词
@log("提问词生成中... (2/2)")
async def create_prompt(question: str, context: str) -> str:
    prompt_template = f"""
    [已知信息]:
      {context}
    [问题]:
      {question}
    """
    return prompt_template


# 清空对话, 清空向量数据库中的对话相关数据
@log("向量库清除中...")
def gc() -> None:
    vector_db = Chroma(persist_directory=db_addr)
    vector_db.delete_collection()
    print("[System] GC回收完毕")