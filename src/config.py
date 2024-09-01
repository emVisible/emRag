from os import getenv

algorithm = getenv("ALGORITHM")
secret_key = str(getenv("SECRET_KEY"))
access_token_expire_minutes = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

k = int(getenv("K")) or 5
chunk_size = getenv("CHUNK_SIZE") or 512
chunk_overlap = getenv("CHUNK_OVERLAP") or 50

db_addr = getenv("DB_ADDR")
doc_addr = getenv("DOC_ADDR")
temp_file_addr = getenv("TEMP_FILE_ADDR")


xinference_addr = getenv("XINFERENCE_ADDR") or "http://127.0.0.1:9997"
xinference_llm_model_id = getenv("XINFERENCE_LLM_MODEL_ID")
xinference_rerank_model_id = (
    getenv("XINFERENCE_RERANK_MODEL_ID") or "bge-reranker-v2-m3"
)
xinference_embedding_model_id = (
    getenv("XINFERENCE_EMBEDDING_MODEL_ID") or "bge-large-zh-v1.5"
)

chroma_addr = getenv("CHROMA_ADDR") or "http://127.0.0.1:8080"
