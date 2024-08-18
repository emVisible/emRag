from json import dumps, loads
from os import getenv

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from starlette.responses import StreamingResponse
from xinference.client import RESTfulClient

from ..utils import Tags
from .dto.chat import ChatDto
from ..config import xinference_addr, xinference_llm_model_id

route_llm = APIRouter(prefix="/llm")


@route_llm.post(
    "/chat",
    summary="[LLM] 通过xinference与模型对话",
    response_description="返回对话结果",
    status_code=status.HTTP_200_OK,
    tags=[Tags.llm],
)
async def chat(body: ChatDto):
    prompt = body.prompt
    system_prompt = body.system_prompt
    chat_history = body.chat_history

    # 通过XINFERENCE Client联通, 对LLM模型发送chat API
    client = RESTfulClient(base_url=xinference_addr or "http://127.0.0.1:9997")
    model = client.get_model(model_uid=xinference_llm_model_id or "qwen2-instruct")
    res = model.chat(
        prompt=prompt,
        system_prompt=system_prompt
        or """你是浙江外国语学院(浙外)问答助手, 根据用户提供的上下文信息, 负责准确回答师生的提问, 对于有已知信息需要筛选的, 给出原数据结果""",
        chat_history=chat_history,
        generate_config={
            "stream": True,
            "max_tokens": 1024,
        },
    )

    def streaming_response_iterator():
        for chunk in res:
            cache = dumps(chunk) + "\n"
            yield cache

    return StreamingResponse(
        content=streaming_response_iterator(),
        media_type="application/json",
        status_code=200,
    )


async def chat_none_stream(body: ChatDto):
    prompt = body.prompt
    system_prompt = body.system_prompt
    chat_history = body.chat_history

    # 通过XINFERENCE Client联通, 对LLM模型发送chat API
    client = RESTfulClient(base_url=xinference_addr or "http://127.0.0.1:9997")
    model = client.get_model(model_uid=xinference_llm_model_id or "qwen2-instruct")
    res = model.chat(
        prompt=prompt,
        system_prompt=system_prompt
        or """You are ZISU(浙江外国语学院, 简称浙外) helper, Follow the user's instructions carefully.
        Respond using markdown format, bold important point, response content needs to be travel-related.
        Respond in Chinese""",
        chat_history=chat_history,
    )
    if res:
        return {"data": res, "code": status.HTTP_200_OK, "msg": "成功"}
    else:
        return {"data": "no data", "code": status.HTTP_400_BAD_REQUEST, "msg": "暂无"}
