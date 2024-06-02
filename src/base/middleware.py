from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from fastapi import Request
# from time import time

# 后端跨域白名单
origins = ["http://127.0.0.1:5173"]

# 示例: 在全局请求添加X-Process-Time header头, value为路由用时
# class TimeMiddleWare(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start_time = time()
#         response = await call_next(request)
#         consume_time = time() - start_time
#         response.headers.append("X-Process-Time", str(consume_time))
#         return response


