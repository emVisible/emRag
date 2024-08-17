from os import getenv
from os.path import join, abspath
from dotenv import load_dotenv

class RAGConfig:
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    QUERY_QUANTITY = 5
