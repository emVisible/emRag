from os import getenv
from os.path import join, abspath
from dotenv import load_dotenv

env_path = join(abspath("./"), ".env")
load_dotenv(dotenv_path=env_path)


class PathConfig:
    DOC_ADDR = getenv("DOC_ADDR") or "docs"
    DB_ADDR = getenv("DB_ADDR") or "db_vector"


class RAGConfig:
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 10


def log_msg():
    max_length = 200
    print(f"[RAG-CONFIG] root path: {env_path}".ljust(max_length))
    print(f"[RAG-CONFIG] doc path: {PathConfig.DOC_ADDR}".ljust(max_length))
    print(f"[RAG-CONFIG] db path: {PathConfig.DB_ADDR}".ljust(max_length))


log_msg()
