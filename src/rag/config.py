from os import getenv
from os.path import join, abspath
from dotenv import load_dotenv

env_path = join(abspath("./"), ".env")
load_dotenv(dotenv_path=env_path)


class PathConfig:
    MODEL_PATH = getenv("MODEL_PATH", "THUDM/chatglm3-6b")
    DOC_ADDR = getenv("DOC_ADDR", "docs")
    DB_ADDR = getenv("DB_ADDR", "db_vector")


class RAGConfig:
    EMBEDDING_MODEL_PATH = getenv(
        "EMBEDDING_PATH", "shibing624_text2vec-base-chinese-paraphrase"
    )
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 10


def log_msg():
    max_length = 200
    print(f"[RAG-CONFIG] root path: {env_path}".ljust(max_length))
    print(f"[RAG-CONFIG] llm model path: {PathConfig.MODEL_PATH}".ljust(max_length))
    print(
        f"[RAG-CONFIG] embedding model path: {RAGConfig.EMBEDDING_MODEL_PATH}".ljust(
            max_length
        )
    )
    print(f"[RAG-CONFIG] doc path: {PathConfig.DOC_ADDR}".ljust(max_length))
    print(f"[RAG-CONFIG] db path: {PathConfig.DB_ADDR}".ljust(max_length))


log_msg()