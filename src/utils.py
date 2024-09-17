from enum import Enum
from logging import CRITICAL, StreamHandler, getLogger
from os import getenv
from os.path import abspath, join
from typing import Any, Optional, Union

from colorlog import ColoredFormatter
from fastapi import status
from pydantic import BaseModel

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

logger = getLogger("fastapi")
logger.handlers.clear()
console_handler = StreamHandler()
console_handler.setFormatter(formatter)
logger.setLevel(CRITICAL)
logger.addHandler(console_handler)


# TODO: 路由使用response_model作为统一相应模型
class ResponseModel(BaseModel):
    data: Optional[Union[str, Any]] = None
    code: int = status.HTTP_200_OK
    msg: str = "ok"


def log(text: str):
    def outer(func):
        def inner(*args, **kwargs):
            print(f"[System] {text}")
            return func(*args, **kwargs)

        return inner

    return outer


def log_msg():
    env_path = join(abspath("./"), ".env")
    logger.critical(f"[AUTH-ALGORITHM] {getenv('ALGORITHM')}")
    logger.critical(f"[AUTH-SECRET KEY] {getenv('SECRET_KEY')}")
    logger.critical(
        f"[AUTH-ACCESS TOKEN EXPIRE TIME] {getenv('ACCESS_TOKEN_EXPIRE_MINUTES')}"
    )
    logger.critical(f"[PATH-ROOT] {env_path}")
    logger.critical(f"[PATH-DB] {getenv('DB_ADDR')}")
    logger.critical(f"[PATH-DOC] {getenv('DOC_ADDR')}")

    logger.critical(f"[RAG-PARAM] k: {getenv('K')}")
    logger.critical(f"[RAG-PARAM] chunk_size: {getenv('CHUNK_SIZE')}")
    logger.critical(f"[RAG-PARAM] chunk_overlap: {getenv('CHUNK_OVERLAP')}")

    logger.critical(f"[XINFERENCE] xinference url: {getenv('XINFERENCE_ADDR')}")
    logger.critical(
        f"[XINFERENCE] xinference llm model id: {getenv('XINFERENCE_LLM_MODEL_ID')}"
    )
    logger.critical(
        f"[XINFERENCE] xinference embedding model id: {getenv('XINFERENCE_EMBEDDING_MODEL_ID')}"
    )
    logger.critical(
        f"[XINFERENCE] xinference rerank model id: {getenv('XINFERENCE_RERANK_MODEL_ID')}"
    )
    logger.critical(f"[VECTOR_DATABASE] chroma url: {getenv('CHROMA_ADDR')}")


# 路由标签
class Tags(Enum):
    dev = "DEV"
    rag = "RAG"
    llm = "LLM"
    user = "User"
    auth = "Auth"
    vector_db = "Vector Database"
    init = "Initialization"
