from os.path import abspath
from dotenv import load_dotenv, get_key

load_dotenv()
class PathConfig:
    _model_path = get_key("./.env", "MODEL_PATH")
    if not _model_path or len(_model_path) == 0:
        MODEL_PATH = "THUDM/chatglm3-6b"
    else:
        MODEL_PATH = abspath(_model_path)

    DOC_ADDR = abspath("./docs")
    DB_ADDR = abspath("./db_vector")


class RAGConfig:
    EMBEDDING_MODEL = "./shibing624_text2vec-base-chinese-paraphrase"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 10