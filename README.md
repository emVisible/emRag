基于LangChain + Xinference构建的本地知识库项目

## 概述
项目旨在搭建一个基于LLM的检索增强生成的知识库QA系统
业务人员导入文档作为检索数据源, 模型提供基础能力, 以此来高效地解决实际生活中的问答情景

显存占用:
以vLLM为Engine, 目前配置 3090x2:
- LLM:       qwen2-instruct(7b)   (21G)  卡0
- Embedding: bge-large-zh-v1.5    (1.5G) 卡1
- Rerank:    bge-reranker-v2-gemma(11G)  卡1

实测7b的显存占用, 提问时的显存峰值接近24G, 单放到一张3090里可能会不稳定

计划未来版本更新:
- Chroma向量数据库 || Redis向量数据库

## 技术栈
LLM:
- LangChain
- Xinference
- Chroma

Python Web:
- FastApi
- pydantic

## 项目目录
```
|- db_vector 向量数据库
|- docs      外部文档
|- src
  |- base
    |- auth     权限相关
      | service_auth
    | controller
    | database    数据库Engine
    | exceptions  容错处理
    | middleware
    | models      Models
    | schemas     Schemas
    | service_init
    | service_user
  |- llm        大模型相关
  |- rag        RAG相关
    |- dto        数据传输对象
    | controller
    | service
    | config      配置类
    | document_loader  文档向量化loader
  | utils       工具函数
|  tmp          临时上传文件
|  .env         环境变量
|  main         入口文件
|  requirements 依赖
|  sql_app.db   sqlite文件
```
## 依赖安装
所需依赖安装
```
  # 安装项目所需依赖
  > pip install -r requirements.txt
```

模型安装(基于XINFERENCE)
按最低配置, 较低档次的16G内存的核显轻薄本完全可以流畅运行, 内存占用大概会到90%, 运行时关掉其它内存占用较大的应用
低配置的LLM问答输出会较慢, 这是正常的
打开本地9997端口, 下载两个模型:
   - LLM模型: Qwen2-instruct
     - Model Engine: vLLM
     - Model Format: pytorch
     - Model Size: 根据自己电脑情况选, 越大性能要求越高
     - Quantization: 同上, None性能要求最高
     - N-GPU: auto
     - Replica: 1
   - Embedding模型: Bge-large-zh-v1.5
     - 按默认下载, CPU运行的, Device中选择CPU
   - Rerank模型: Bge-reranker-v2-m3

## 项目启动
启动项目
```
  > uvicorn main:app --port 3000 --reload
```

进入swagger文档
```
  > http://127.0.0.1:3000/docs
```

启动Xinference
Linux下启动
```
  > XINFERENCE_MODEL_SRC=modelscope xinference-local --host 0.0.0.0 --port 9997
```
选择对应模型
windows下启动
```
  设置环境变量
  > set XINFERENCE_MODEL_SRC=modelscope
  启动
  > xinference-local --host 127.0.0.1 --port 9997
```

tip: 清除python进程
```
  > ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill -9
```

启动Chroma
```
  > chroma run --path ./db_vector --port 8080
```

### 启动问题
启动xinference时遇到报错:
1. 升级gcc和g++到11版本
   - 针对llama_cpp_python成功安装但是xinference启动报错
2. 手动下载llama_cpp_python
   - 遇到llama_cpp或者chaglm_cpp的whl问题, 需要前往chatglm_cpp和llama_cpp_python这两个github repo中手动下载对应版本, 并通过pip安装

## 并发测试
LLM测试
12线程400链接, 600秒测试, 10分钟内可处理1000个请求, 平均每秒处理1.7个对话请求, 每个回答大约有700左右的字数
```
  > wrk -t12 -c400 -d600 -s ./test.lua http://127.0.0.1:3000/api/llm/chat

  Running 10m test @ http://localhost:3000/api/llm/chat
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     0.00us    0.00us   0.00us    -nan%
    Req/Sec     0.24      0.96    10.00     95.09%
  1039 requests in 10.00m, 6.64MB read
  Socket errors: connect 0, read 0, write 0, timeout 1039
  Requests/sec:      1.73
  Transfer/sec:     11.33KB
```
RAG测试