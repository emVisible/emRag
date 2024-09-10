from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse
from torch.cuda import empty_cache, ipc_collect, is_available

from src.base.controller import route_base
from src.base.database import engine
from src.base.middleware import CORSMiddleware, origins
from src.base.models import Base
from src.init.controller import route_init
from src.llm.controller import route_llm
from src.rag.controller import route_rag
from src.utils import log_msg, logger
from src.vector_store.controller import route_vector


@asynccontextmanager
async def lifespan(app: FastAPI):
    if is_available():
        logger.critical("CUDA is available. Initializing...")
    else:
        logger.critical("CUDA not available. Proceeding without GPU.")
    yield
    if is_available():
        empty_cache()
        ipc_collect()


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swaqqer-ui/5.6.2/swagqer-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.6.2/swagger-ui.min.css",
        *args,
        **kwargs
    )


load_dotenv("./.env")
# 打印配置信息
log_msg()
# 初始化数据库
Base.metadata.create_all(bind=engine)
# 初始化app实例
app = FastAPI(title="ZISU-RAG", version="1.0.0", lifespan=lifespan)
# 导入路由
route_prefix = "/api"
app.include_router(route_base, prefix=route_prefix)
app.include_router(route_init, prefix=route_prefix)
app.include_router(route_vector, prefix=route_prefix)
app.include_router(route_llm, prefix=route_prefix)
app.include_router(route_rag, prefix=route_prefix)
# 跨域中间件
app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/")
def root_page():
    return RedirectResponse("/docs")


@app.get("/docs", include_in_schema=False)
def custom_swagger():
    return swagger_monkey_patch(app.openapi())
