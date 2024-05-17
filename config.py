from enum import Enum
from os.path import abspath
from dotenv import get_key


class PathConfig(Enum):
    MODEL_PATH = "THUDM/chatglm3-6b"
    DOC_ADDR = abspath("./docs")
    DB_ADDR = abspath("./db_vector")


class RAGConfig(Enum):
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 3
