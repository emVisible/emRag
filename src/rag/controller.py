from fastapi import APIRouter, status

from src.llm.controller import chat

from ..llm.dto.chat import ChatDto
from ..utils import Tag
from . import service
from .dto.completion import CompletionDto
from .generateDB import run

route_rag = APIRouter(prefix="/rag")


"""
  1. 调用Langchain, 检索文档
  2. 合成Prompt
  3. 调用LLM, 返回结果
"""


@route_rag.post(
    "/chat",
    summary="[RAG] 对话",
    response_description="返回最终结果",
    status_code=status.HTTP_200_OK,
    tags=[Tag.rag],
)
async def search(body: CompletionDto):
    prompt = body.prompt
    context = await service.similarity_search(question=prompt)
    prompt = await service.create_prompt(question=prompt, context=context)
    print(prompt)
    result = await chat(body=ChatDto(prompt=prompt))
    return {"data": result, "code": status.HTTP_200_OK, "msg": "暂无"}


@route_rag.post(
    "/generate",
    summary="[RAG] 批量创建矢量库",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tag.rag],
)
async def generate():
    run()


@route_rag.post(
    "/gc",
    summary="[RAG] 清空数据库",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tag.rag],
)
async def gc():
    status = service.gc()
    if status == 1:
        return {"data": "GC回收OK", "code": status.HTTP_200_OK, "msg": "暂无"}
