基于LangChain + ChatGLM3构建本地知识库

## 概述
项目旨在搭建一个基于LLM的检索增强生成的知识库QA系统
业务人员导入文档作为检索数据源, 模型提供基础能力, 以此来高效地解决实际生活中的问答情景

## 技术栈
LLM:
- LangChain
- ChatGLM3
后端功能:
- FastApi
- pydantic
文档:
- swagger (通过外网CDN加载)

## 项目目录
|- db_vector 向量数据库
|- docs      外部文档
|- src
  |- dto        数据传输对象
  |- llm        GLM3模型相关代码
    |  glm      GLM3模型类
    |  llm      GLM3路由与服务
    |  utils    工具函数
  |  controller 控制器
  |  service    服务
  |  utils      工具函数
|  .env         环境变量
|  automation   自动化脚本
|  config       配置类
|  main         入口文件
|  requirements 依赖

## 项目启动
```
  # 安装项目所需依赖
  > pip install -r requirements.txt
```

```
  # 启动项目
  > python main.py
```

```
  进入swagger文档
  > http://127.0.0.1:3000/docs
```