from ..config import xinference_addr, xinference_llm_model_id, xinference_rerank_model_id
from xinference.client import RESTfulClient

client = RESTfulClient(base_url=xinference_addr or "http://127.0.0.1:9997")
llm_model = client.get_model(model_uid=xinference_llm_model_id or "qwen2-instruct")
rerank_model = client.get_model(model_uid=xinference_rerank_model_id)