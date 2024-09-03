from asyncio import Lock, Semaphore, sleep
from json import dumps

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from src.xinference.service import llm_model

from ..config import system_prompt_rag
from ..llm.dto.chat import ChatDto
from ..utils import Tags
from . import service

route_rag = APIRouter(prefix="/rag")
model_lock = Lock()
semaphore = Semaphore(5)


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
async def search(body: ChatDto):
    prompt = body.prompt
    chat_history = body.chat_history

    context = await service.similarity_search(question=prompt)
    prompt = await service.create_prompt(question=prompt, context=context)

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
