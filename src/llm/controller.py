from asyncio import Lock, Semaphore, sleep
from json import dumps

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from starlette.responses import StreamingResponse

from src.xinference.service import llm_model

from ..prompt import system_prompt_llm
from ..utils import Tags
from .dto.chat import LLMChatDto

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
async def chat(body: LLMChatDto):
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