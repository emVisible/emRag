from datetime import timedelta
from enum import Enum

from dotenv import dotenv_values
from fastapi import APIRouter, Body, Depends, HTTPException, status

from . import service
from .dto.completion import CompletionDto

route = APIRouter(prefix="/core")


class Tag(Enum):
    llm = "LLM"
    langchain = "LangChain"


@route.post(
    "/completion",
    summary="对话",
    response_description="返回最终结果",
    status_code=status.HTTP_200_OK,
    tags=[Tag.llm],
)
async def search(body: CompletionDto):
    prompt = body.prompt
    context = await service.similarity_search(question=prompt)
    result = await service.ask_to_llm(question=prompt, context=context)
    return {"data": result, "code": status.HTTP_200_OK, "msg": "暂无"}