import chromadb
from src.config import db_addr


def get_client():
    persistent_client = chromadb.PersistentClient(path=db_addr)
    return persistent_client
