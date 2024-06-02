from enum import Enum
from fastapi import APIRouter,  status
from . import service
from .dto.completion import CompletionDto

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
