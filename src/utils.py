def log(text: str):
    def outer(func):
        def inner(*args, **kwargs):
            print(f"[System] {text}")
            return func(*args, **kwargs)
        return inner
    return outer


def log_path(MODEL_PATH, TOKENIZER_PATH, EMBEDDING_PATH):
  max_length = 200
  print(f"[LLM-CONFIG] llm model path: {MODEL_PATH}".ljust(max_length))
  print(f"[LLM-CONFIG] tokenizer model path: {TOKENIZER_PATH}".ljust(max_length))
  print(f"[LLM-CONFIG] embedding model path: {EMBEDDING_PATH}".ljust(max_length))