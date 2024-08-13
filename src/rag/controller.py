from enum import Enum
from fastapi import APIRouter, status
from . import service
from .dto.completion import CompletionDto
from .dto.chat import ChatDto
from xinference.client import RESTfulClient

route_rag = APIRouter(prefix="/rag")


class Tag(Enum):
    rag = "RAG"


@route_rag.post(
    "/completion",
    summary="[RAG] 对话",
    response_description="返回最终结果",
    status_code=status.HTTP_200_OK,
    tags=[Tag.rag],
)
async def search(body: CompletionDto):
    prompt = body.prompt
    context = await service.similarity_search(question=prompt)
    result = await service.create_prompt(question=prompt, context=context)
    return {"data": result, "code": status.HTTP_200_OK, "msg": "暂无"}


@route_rag.post(
    "/gc",
    summary="[RAG] 清空数据库",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tag.rag],
)
async def gc():
    status = await service.gc()
    if status == 1:
        return {"data": "GC回收OK", "code": status.HTTP_200_OK, "msg": "暂无"}


@route_rag.post(
    "/chat",
    summary="[RAG] 通过xinference与模型对话",
    response_description="返回对话结果",
    status_code=status.HTTP_200_OK,
    tags=[Tag.rag],
)
async def chat(body: ChatDto):
    prompt, system_prompt, chat_history = body
    print(body)
    client = RESTfulClient("http://127.0.0.1:9997")
    model = client.get_model("qwen2-instruct")
    res = model.chat(prompt=prompt, system_prompt=system_prompt, chat_history=chat_history)
    if res:
        return {"data": res, "code": status.HTTP_200_OK, "msg": "成功"}
    else:
        return {"data": "no data", "code": status.HTTP_400_BAD_REQUEST, "msg": "暂无"}
