基于LangChain + Xinference构建的本地知识库项目

## 概述
项目旨在搭建一个基于LLM的检索增强生成的知识库QA系统
业务人员导入文档作为检索数据源, 模型提供基础能力, 以此来高效地解决实际生活中的问答情景

显存占用:
以当前默认模型, 显存占用约20G, Nvidia 3090(24G)可在全启动情况下以开发模式正常运行:
- LLM:       Qwen2-instruct(7b), 显存占用15G
- Embedding: bge-large-zh-v1.5, 显存占用1.6G
- Rerank:    bge-reranker-v2-m3, 显存占用2.7G

计划未来版本更新:
- Milvus向量数据库

## 技术栈
LLM:
- LangChain
- Xinference

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
遇到llama_cpp或者chaglm_cpp的whl问题, 需要前往chatglm_cpp和llama_cpp_python这两个github repo中手动下载对应版本, 并通过pip安装

模型安装(基于XINFERENCE)
按最低配置, 较低档次的16G内存的核显轻薄本完全可以流畅运行, 内存占用大概会到90%, 运行时关掉其它内存占用较大的应用
低配置的LLM问答输出会较慢, 这是正常的
打开本地9997端口, 下载两个模型:
   - LLM模型: Qwen2-instruct
     - Model Engine: transformers
     - Model Format: pytorch
     - Model Size: 根据自己电脑情况选, 越大性能要求越高
     - Quantization: 同上, None性能要求最高
     - N-GPU: auto
     - Replica: 1
   - Embedding模型: Bge-large-zh-v1.5
     - 按默认下载, CPU运行的, Device中选择CPU

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