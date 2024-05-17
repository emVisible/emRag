import os
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# 加载配置
output_dir = os.getenv("DB_ADDR")
embedding_model = os.getenv("EMBEDDING_MODEL")
query_quantity = os.getenv("QUERY_QUANTITY")


def init():
    pass


# 通过文本转换为向量, 生成结果
async def search_rag(question: str) -> str:
    embedding_function = SentenceTransformerEmbeddings(model_name=embedding_model)
    db = Chroma(persist_directory=output_dir, embedding_function=embedding_function)

    question = f"{question or '介绍一下杭州'}"
    context = db.similarity_search(query=question, k=query_quantity)
    res = ""
    for chunk, i in context:
        print(f"chunk[{i}]元数据: {chunk.metadata}")
        res += chunk.page_content
    return res

async def ask_llm(question: str)->str:
  pass

# 清空对话
async def gc() -> None:
    vector_db = Chroma(persist_directory=output_dir)
    vector_db.delete_collection()
    vector_db.persist()
    print("[System] GC回收完毕")
