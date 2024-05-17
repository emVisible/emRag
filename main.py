from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.controller import route
# from src.llm.llm import llm_route


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swaqqer-ui/5.6.2/swagqer-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.6.2/swagger-ui.min.css"
    )


# 初始化app实例
app = FastAPI(title="pracLangchain", version="1.0.0")
# 导入路由
app.include_router(route, prefix="/api")
# app.include_router(llm_route, prefix="/api")
# 跨域中间件
app.add_middleware(CORSMiddleware, allow_origins=["127.0.0.1:5173"])


@app.get("/api")
def root_page():
    return {"pracLangchain": "Hello World!"}


def run():
    mode = dotenv_values(".env").get("MODE")
    if mode == "DEV":
        import uvicorn

        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=int(dotenv_values(".env").get("DEV_PORT")),
            reload=True,
        )

    elif mode == "PRO":
        import uvicorn

        uvicorn.run(
            "main:app", host="0.0.0.0", port=int(dotenv_values(".env").get("PRO_PORT"))
        )
    else:
        raise RuntimeError("Please check the .env file.")


if __name__ == "__main__":
    run()
