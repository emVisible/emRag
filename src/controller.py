from fastapi import status, HTTPException, Depends, APIRouter, Body
from enum import Enum
from datetime import timedelta
from dotenv import dotenv_values
from . import service
from .dto import CompletionDto

route = APIRouter(prefix='/core')


class Tag(Enum):
    llm = "LLM"
    langchain = "LangChain"


@route.post(
    "/completion",
    summary="对话",
    # response_model=CompletionDto,
    response_description="返回最终结果",
    status_code=status.HTTP_200_OK,
    tags=[Tag.llm],
)

async def search(body: CompletionDto):
    [prompt] = body
    rag_result = await service.search_rag(prompt)
    msg_result = await service.ask_llm(rag_result)
    return {"data": msg_result, "code": status.HTTP_200_OK, "msg": "暂无"}