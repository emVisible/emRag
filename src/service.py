import os

from langchain import hub
from langchain.agents import (AgentExecutor, create_structured_chat_agent,
                              load_tools)
from langchain.embeddings.sentence_transformer import \
    SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.messages import AIMessage, HumanMessage

from .llm.glm import ChatGLM3
from .utils import log

from config import PathConfig, RAGConfig

# 加载配置
db_addr = PathConfig.DB_ADDR
query_quantity = RAGConfig.QUERY_QUANTITY
model_path = PathConfig.MODEL_PATH


# 通过LangChain加载ChatGLM3模型
@log("ChatGLM3模型加载中... (init)")
def load_glm():
    llm = ChatGLM3()
    llm.load_model(model_path)
    prompt = hub.pull("hwchase17/structured-chat-agent")
    tools = []

    # 实例代理
    agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    return agent_executor


# rag文档检索, 通过文本转换为向量, 生成结果
@log("RAG搜索中... (1/2)")
async def similarity_search(question: str) -> str:
    res = ""
    # 向量数据库初始化: 嵌入函数、数据库实例、提问文本
    embedding_function = SentenceTransformerEmbeddings(model_name=model_path)
    db = Chroma(persist_directory=db_addr, embedding_function=embedding_function)
    question = f"{question or '介绍一下杭州'}"
    # 从向量数据库中查询相关信息
    context = db.similarity_search(query=question, k=query_quantity)
    # 对最终结果进行累加
    for chunk, i in context:
        print(f"chunk[{i}]元数据: {chunk.metadata}")
        res += chunk.page_content
    return res


# 结合模糊搜索的结果, 与大模型对话得出答案
@log("模型回答中... (2/2)")
async def ask_to_llm(question: str, context:str) -> str:
    # 获取模糊搜索结果, 作为向模型传输的上下文
    prompt_template = f"""
    你现在扮演一名辅助教师, 细心听着以下的问题作出解答,
    如若无法从信息中提取相关的答案, 请说\"无法回答该问题\"之类的话语:
    已知信息:
    {context}
    问题:
    {question}
    """

    # 加载模型
    agent = load_glm()
    # 向模型发送模板请求
    res = agent.invoke(prompt_template)
    return res


# 清空对话, 清空向量数据库中的对话相关数据
@log("清理会话中...")
def gc() -> None:
    vector_db = Chroma(persist_directory=db_addr)
    vector_db.delete_collection()
    vector_db.persist()
    print("[System] GC回收完毕")