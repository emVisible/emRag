from os.path import abspath
from dotenv import load_dotenv, get_key

load_dotenv()
class PathConfig:
    # 获取 .env 文件中的 MODEL_PATH 值，如果不存在则使用默认值
    _model_path = get_key(".env", "MODEL_PATH")
    if not _model_path or len(_model_path) == 0:
        MODEL_PATH = "THUDM/chatglm3-6b"
    else:
        MODEL_PATH = abspath(_model_path)

    DOC_ADDR = abspath("./docs")
    DB_ADDR = abspath("./db_vector")


class RAGConfig:
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 3