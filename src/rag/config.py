from os.path import abspath
from dotenv import load_dotenv, get_key

load_dotenv()


class PathConfig:
    _model_path = get_key(".env", "MODEL_PATH")
    MODEL_PATH = abspath(_model_path) or "THUDM/chatglm3-6b"
    DOC_ADDR = abspath("docs")
    DB_ADDR = abspath("db_vector")


class RAGConfig:
    _embedding_path = get_key(".env", "EMBEDDING_PATH")
    EMBEDDING_MODEL_PATH = (
        abspath(_embedding_path) or "shibing624_text2vec-base-chinese-paraphrase"
    )
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 10
