from src.base.database import engine
from src.base.middleware import CORSMiddleware, origins
from src.base.models import Base
from src.base.controller import route_base
from src.rag.controller import route_rag
from src.llm.controller import route_llm
from src.utils import log_msg
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import torch


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


# Swagger文档
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swaqqer-ui/5.6.2/swagqer-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.6.2/swagger-ui.min.css"
        * args,
        **kwargs
    )

# 打印配置信息
log_msg()
# 初始化数据库
Base.metadata.create_all(bind=engine)
# 初始化app实例
app = FastAPI(title="ZISU-RAG", version="1.0.0", lifespan=lifespan)
route_prefix = "/api"
# 导入路由
# app.include_router(route_base, prefix=route_prefix)
app.include_router(route_rag, prefix=route_prefix)
app.include_router(route_llm, prefix=route_prefix)
# 跨域中间件
# app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/")
def root_page():
    return RedirectResponse("/docs")