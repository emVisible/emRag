from enum import Enum
from os.path import abspath


class PathConfig(Enum):
    DOC_ADDR = abspath("./docs")
    EMBEDDING_MODEL = abspath("...")
    MODEL_PATH = abspath("...")
    DB_ADDR = abspath("./db_vector")


class RAGConfig(Enum):
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 3