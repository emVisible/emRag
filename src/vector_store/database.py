import chromadb
from src.config import db_addr
def get_client():
    return chromadb.Cliet(path=db_addr)