from asyncio import Lock, sleep
from json import dumps

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from src.xinference.service import llm_model

from ..config import max_model_len
from ..llm.dto.chat import RAGChatDto
from ..prompt import system_prompt_rag
from ..utils import Tags
from . import service

route_rag = APIRouter(prefix="/rag")

model_lock = Lock()

"""
  1. 调用LangChain, 检索文档
  2. 调用Rerank Model, 对结果排序
  3. 合成提问Prompt
  4. 调用LLM, 返回结果
"""


@route_rag.post(
    "/chat",
    summary="[RAG] 对话",
    response_description="返回最终结果",
    status_code=status.HTTP_200_OK,
    tags=[Tags.rag],
)
async def search(body: RAGChatDto):
    raw_prompt = body.prompt
    chat_history = body.chat_history
    collection_name = body.collection_name
    context = await service.similarity_search(
        question=raw_prompt, collection_name=collection_name
    )
    prompt = await service.create_system_dynamic_prompt(
        question=raw_prompt, context=context
    )
    if len(prompt) > int(max_model_len):
        prompt = prompt[:max_model_len]
    async with model_lock:
        res = llm_model.chat(
            prompt=prompt,
            system_prompt=system_prompt_rag,
            chat_history=chat_history,
            generate_config={
                "stream": True,
                "max_tokens": 1024,
            },
        )

    async def streaming_response_iterator():
        for chunk in res:
            cache = dumps(chunk["choices"][0]["delta"]["content"]) + "\n"
            if cache:
                yield cache
            await sleep(0)

    return StreamingResponse(
        content=streaming_response_iterator(),
        media_type="text/event-stream",
        status_code=200,
    )
