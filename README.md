# LexiNaut

基于LangChain + Xinference + Chroma构建的本地知识库项目

## 概述

项目旨在搭建一个RAG本地知识库系统, 基于FastAPI进行API拓展开发
业务人员导入文档作为检索数据源, 模型提供基础储存、检索、回答能力, 以此来高效地解决实际生活中的问答情景

示例配置( 服务器 / 正常开发 ):

- GPU: 3090 x 2
- Engine: vLLM
- LLM:       qwen2-instruct(7b)          卡0
- Embedding: bge-large-zh-v1.5    (1.5G) 卡1
- Rerank:    bge-reranker-v2-gemma(11G)  卡1

示例配置( 节约开发 / 本地 ):

- GPU: 3090x1 或 笔记本自带显卡
- Engine: Transformers
- LLM:       qwen2-instruct(1.5b)
- Embedding: bge-large-zh-v1.5
- Rerank:    bge-reranker-base_v1

## 依赖安装

所需依赖安装

``` bash
  pip install -r requirements.txt
```

模型安装 (XINFERENCE)
低配置的LLM问答输出会较慢, 这是正常的
打开本地9997端口, 下载两个模型:

- LLM模型: qwen2-instruct
  - Model Engine: vLLM
  - Model Format: pytorch
  - Model Size: 根据自己电脑情况选, 越大性能要求越高
  - Quantization: 同上, None性能要求最高
  - N-GPU: auto
  - Replica: 1
- Embedding模型: bge-large-zh-v1.5
  - 按默认下载, CPU运行的, Device中选择CPU
- Rerank模型: bge-reranker-v2-m3 或 bge-reranker-v2-gemma

## 项目启动

切换至对应环境

``` bash
  conda activate lexinaut
```

### Xinference

Linux下启动

``` bash
  XINFERENCE_MODEL_SRC=modelscope xinference-local --host 0.0.0.0 --port 9997
```

windows下启动

``` shell
  set XINFERENCE_MODEL_SRC=modelscope
```

``` bash
  xinference-local --host 127.0.0.1 --port 9997
```

启动LLM、Embedding、Rerank模型:

- LLM: 添加参数max_model_len, RAG搜索时的input token数量

### 项目

``` bash
  uvicorn main:app --port 3000 --reload
```

### Chroma

```bash
  chroma run --path ./db_vector --port 8080
```

### GPU信息

``` bash
  watch nvidia-smi
```

### 问题一览

启动xinference时遇到报错:

1. 升级gcc和g++到11版本
   - 针对llama_cpp_python成功安装但是xinference启动报错
2. 手动下载llama_cpp_python
   - 遇到llama_cpp或者chaglm_cpp的whl问题, 需要前往chatglm_cpp和llama_cpp_python这两个github repo中手动下载对应版本, 并通过pip安装
3. Xinference Web UI在模型的GPU Index选择时会有JS的Bug, 需要手动输入两次再点启动
4. 服务器卡顿退出, 服务仍在运行时, 清除python程序:

   ``` bash
      ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill -9
   ```

5. torch与torchvision版本需要匹配: 0.23.0对应0.18.0

## 并发测试

12线程400链接, 600秒测试

LLM测试结果:
GPU功率峰值可达280W, 平均在220W左右
单张3090压力测试下, 最高平均响应约为1200tokens/s, 最多每秒同时响应120 request
每秒在100对话并发情况下, 平均每个请求每秒响应10个字左右
可处理1000个左右请求, 平均每秒处理1.7个对话请求 (每个回答大约有700左右的字数)

``` bash
  > wrk -t12 -c400 -d600 -s ./llm.lua http://127.0.0.1:3000/api/llm/chat

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
