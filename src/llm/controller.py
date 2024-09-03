from json import dumps, loads
from os import getenv

from fastapi import APIRouter, status, WebSocket
from fastapi.responses import StreamingResponse
from starlette.responses import StreamingResponse
from xinference.client import RESTfulClient
from asyncio import Lock, sleep, Semaphore
from src.xinference.service import llm_model


from ..utils import Tags
from .dto.chat import ChatDto
from ..config import xinference_addr, xinference_llm_model_id, system_prompt_llm

route_llm = APIRouter(prefix="/llm")
model_lock = Lock()
semaphore = Semaphore(5)


@route_llm.post(
    "/chat",
    summary="[LLM] 通过xinference与模型对话",
    response_description="返回对话结果",
    status_code=status.HTTP_200_OK,
    tags=[Tags.llm],
)
async def chat(body: ChatDto):
    prompt = body.prompt
    chat_history = body.chat_history

    # 通过XINFERENCE Client联通, 对LLM模型发送chat API
    async with model_lock:
        res = llm_model.chat(
            prompt=prompt,
            system_prompt=system_prompt_llm,
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


async def chat_none_stream(body: ChatDto):
    prompt = body.prompt
    chat_history = body.chat_history

    # 通过XINFERENCE Client联通, 对LLM模型发送chat API
    res = llm_model.chat(
        prompt=prompt,
        system_prompt=system_prompt_llm,
        chat_history=chat_history,
    )
    if res:
        return {"data": res, "code": status.HTTP_200_OK, "msg": "成功"}
    else:
        return {"data": "no data", "code": status.HTTP_400_BAD_REQUEST, "msg": "暂无"}
