def log(text: str):
    def outer(func):
        def inner(*args, **kwargs):
            print(f"[System] {text}")
            return func(*args, **kwargs)
        return inner
    return outer
