from os import getenv
from os.path import dirname, join

from dotenv import load_dotenv

base_dir = dirname(__file__)
env_path = join(base_dir, ".env")
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
