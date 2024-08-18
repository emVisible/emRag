from fastapi import APIRouter, status, File, UploadFile, HTTPException
from pathlib import Path


from src.llm.controller import chat, chat_none_stream

from ..llm.dto.chat import ChatDto
from ..utils import Tags
from . import service
from .dto.completion import CompletionDto
from .document_loader import (
    embedding_all_from_dir,
    embedding_document,
)

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
    tags=[Tags.rag],
)
async def search(body: CompletionDto):
    prompt = body.prompt
    context = await service.similarity_search(question=prompt)
    prompt = await service.create_prompt(question=prompt, context=context)
    result = await chat_none_stream(body=ChatDto(prompt=prompt))
    return {"data": result, "code": status.HTTP_200_OK, "msg": "暂无"}


@route_rag.post(
    "/upload_single",
    summary="[RAG] 根据单一文档转换为矢量",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.rag],
)
async def upload_single(file: UploadFile = File(...)):
    return embedding_document(file)


@route_rag.post(
    "/generate",
    summary="[RAG] 批量创建矢量库",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.rag],
)
async def generate():
    embedding_all_from_dir()


@route_rag.post(
    "/gc",
    summary="[RAG] 清空数据库",
    response_description="返回是否成功",
    status_code=status.HTTP_200_OK,
    tags=[Tags.rag],
)
async def gc():
    status = service.gc()
    if status == 1:
        return {"data": "GC回收OK", "code": status.HTTP_200_OK, "msg": "暂无"}
