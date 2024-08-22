from json import dumps

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from xinference.client import RESTfulClient
from asyncio import Lock, sleep, Semaphore

from ..config import xinference_addr, xinference_llm_model_id
from ..llm.dto.chat import ChatDto
from ..utils import Tags
from . import service
from .document_loader import embedding_all_from_dir, embedding_document

route_rag = APIRouter(prefix="/rag")
model_lock = Lock()
client = RESTfulClient(base_url=xinference_addr or "http://127.0.0.1:9997")
model = client.get_model(model_uid=xinference_llm_model_id or "qwen2-instruct")
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
    system_prompt = body.system_prompt
    chat_history = body.chat_history

    context = await service.similarity_search(question=prompt)
    prompt = await service.create_prompt(question=prompt, context=context)

    async with model_lock:
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

    async def streaming_response_iterator():
        for chunk in res:
            cache = dumps(chunk["choices"][0]["delta"]["content"]) + "\n"
            if cache:
                print(cache)
                yield cache
            await sleep(0)  # 确保其他协程有机会运行


    return StreamingResponse(
        content=streaming_response_iterator(),
        media_type="text/event-stream",
        status_code=200,
    )


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
