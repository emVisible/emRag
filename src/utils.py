from enum import Enum
from logging import CRITICAL, INFO, StreamHandler, basicConfig, getLogger
from os import getenv
from os.path import abspath, join
from colorlog import ColoredFormatter

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
config_logger = getLogger("fastapi")
config_logger.handlers.clear()
console_handler = StreamHandler()
console_handler.setFormatter(formatter)
config_logger.setLevel(CRITICAL)
config_logger.addHandler(console_handler)

file_log = basicConfig(
    filename="lexinaut.log",  # 输出日志文件
    level=INFO,  # 日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
)


# 路由标签
class Tags(Enum):
    dev = "DEV"
    rag = "RAG"
    llm = "LLM"
    user = "User"
    auth = "Auth"
    vector_db = "Vector Database"
    init = "Initialization"


class SystemTags(Enum):
    project = "[Project]"
    auth = "[Auth]"
    vector = "[Vector]"
    model = "[Model]"


def log(text: str):
    def outer(func):
        def inner(*args, **kwargs):
            print(f"[System] {text}")
            return func(*args, **kwargs)

        return inner

    return outer


def log_config():
    project = SystemTags.project.value
    auth = SystemTags.auth.value
    vector = SystemTags.vector.value
    model = SystemTags.model.value
    env_path = join(abspath("./"), ".env")
    config_logger.critical(f"[{project}]-[ENV_PATH]-{env_path}")
    configs = [
        {"name": "ENV_PATH", "tags": project},
        {"name": "ALGORITHM", "tags": auth},
        {"name": "SECRECT_KEY", "tags": auth},
        {"name": "ACCESS_TOKEN_EXPIRE_MINUTES", "tags": auth},
        {"name": "DB_ADDR", "tags": vector},
        {"name": "DOC_ADDR", "tags": vector},
        {"name": "CHROMA_ADDR", "tags": vector},
        {"name": "K", "tags": vector},
        {"name": "ALLOW_RESET", "tags": vector},
        {"name": "MIN_RELEVANCE_SCORE", "tags": vector},
        {"name": "XINFERENCE_ADDR", "tags": model},
        {"name": "XINFERENCE_LLM_MODEL_ID", "tags": model},
        {"name": "XINFERENCE_EMBEDDING_MODEL_ID", "tags": model},
        {"name": "XINFERENCE_RERANK_MODEL_ID", "tags": model},
        {"name": "CHUNK_SIZE", "tags": model},
        {"name": "CHUNK_OVERLAP", "tags": model},
        {"name": "MAX_MODEL_LEN", "tags": model},
    ]
    for config in configs:
        tag = config["tags"]
        name = config["name"]
        config_logger.critical(f"[{tag}]-[{name}]: {getenv(name)}")
