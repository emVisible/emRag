基于LangChain + ChatGLM3构建本地知识库

## 概述
项目旨在搭建一个基于LLM的检索增强生成的知识库QA系统
业务人员导入文档作为检索数据源, 模型提供基础能力, 以此来高效地解决实际生活中的问答情景

## 技术栈
LLM:
- LangChain
- Qwen2-instruct(暂定)
后端功能:
- FastApi
- pydantic
文档:
- swagger (通过外网CDN加载)

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