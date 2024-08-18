from enum import Enum
from os import getenv
from os.path import abspath, join
from typing import Any, Optional, Union

from dotenv import load_dotenv
from fastapi import status
from pydantic import BaseModel


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
    load_dotenv(dotenv_path=env_path)
    max_length = 200
    print(f"[PATH-ROOT] root path: {env_path}".ljust(max_length))
    print(f"[PATH-DOC] doc path: {getenv('DOC_ADDR')}".ljust(max_length))
    print(f"[PATH-DB] db path: {getenv('DB_ADDR')}".ljust(max_length))

    print(f"[RAG-CONFIG] xinference url: {getenv('XINFERENCE_ADDR')}".ljust(max_length))
    print(
        f"[RAG-CONFIG] xinference llm model id: {getenv('XINFERENCE_LLM_MODEL_ID')}".ljust(
            max_length
        )
    )
    print(
        f"[RAG-CONFIG] xinference embedding model id: {getenv('XINFERENCE_EMBEDDING_MODEL_ID')}".ljust(
            max_length
        )
    )
    print(
        f"[RAG-CONFIG] xinference rerank model id: {getenv('XINFERENCE_RERANK_MODEL_ID')}".ljust(
            max_length
        )
    )


# 路由标签
class Tags(Enum):
    rag = "RAG"
    llm = "LLM"
    user = "User"
    auth = "Auth"
    dev = "[DEV] 仅限开发"
