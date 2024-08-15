from os import getenv
from .dto.chat import ChatDto
from ..utils import Tag
from fastapi import APIRouter, status
from xinference.client import RESTfulClient

xinference_addr = getenv("XINFERENCE_ADDR")
xinference_llm_model_id = getenv("XINFERENCE_LLM_MODEL_ID")
route_llm = APIRouter(prefix="/llm")


@route_llm.post(
    "/chat",
    summary="[LLM] 通过xinference与模型对话",
    response_description="返回对话结果",
    status_code=status.HTTP_200_OK,
    tags=[Tag.llm],
)
async def chat(body: ChatDto):
    prompt = body.prompt
    system_prompt = body.system_prompt
    chat_history = body.chat_history

    client = RESTfulClient(base_url=xinference_addr or "http://127.0.0.1:9997")
    model = client.get_model(model_uid=xinference_llm_model_id or "qwen2-instruct")
    res = model.chat(
        prompt=prompt,
        system_prompt=system_prompt
        or """你是浙江外国语学院(浙外)问答助手, 根据用户提供的上下文信息, 负责准确回答师生的提问, 对于有已知信息需要筛选的, 给出原数据结果""",
        chat_history=chat_history or [],
    )
    if res:
        return {"data": res, "code": status.HTTP_200_OK, "msg": "成功"}
    else:
        return {"data": "no data", "code": status.HTTP_400_BAD_REQUEST, "msg": "暂无"}
