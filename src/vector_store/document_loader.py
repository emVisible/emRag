# coding: utf-8
import glob
import os
import shutil

# import torch
from multiprocessing import Pool
from pathlib import Path
from typing import List

from fastapi import File, HTTPException, UploadFile
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.embeddings import XinferenceEmbeddings
from tqdm import tqdm

from ..config import (
    chunk_overlap,
    chunk_size,
    db_addr,
    doc_addr,
    xinference_embedding_model_id,
    xinference_addr,
)


# 自定义文档加载器 document loader
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if "text/html content not found in email" in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"] = "text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc


# document loader 映射表
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    ".xls": (UnstructuredExcelLoader, {}),
    ".xlsx": (UnstructuredExcelLoader, {}),
}


# 加载单个文档
def load_document(file_path: str) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()
    raise ValueError(f"不支持的格式 .'{ext}'")


# 加载多个文档
def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    filtered_files = [
        file_path for file_path in all_files if file_path not in ignored_files
    ]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc="文档加载中", ncols=80) as pbar:
            for i, docs in enumerate(
                pool.imap_unordered(load_document, filtered_files)
            ):
                results.extend(docs)
                pbar.update()

    return results


# 批量加载指定目录文档
def process_documents(ignored_files: List[str] = []) -> List[Document]:
    print(f"文档加载中: 源自 {doc_addr}")
    documents = load_documents(doc_addr, ignored_files)
    if not documents:
        print("没有可加载的文档")
        exit(0)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    texts = text_splitter.split_documents(documents)
    print(f"Chunks分割: {len(texts)} (最大为 {chunk_size} tokens)")
    return texts


def embedding_document(file: UploadFile = File(...)):
    tmp_dir = os.getenv("TEMP_FILE_ADDR")
    Path(f"{tmp_dir}").mkdir(parents=True, exist_ok=True)
    tmp_save_path_obj = Path(f"{tmp_dir}/{file.filename}")
    tmp_save_path = str(tmp_save_path_obj)
    try:
        with open(tmp_save_path, "wb") as tmp_f:
            shutil.copyfileobj(file.file, tmp_f)
        documents = load_document(tmp_save_path)
        embedding_function = XinferenceEmbeddings(
            server_url=xinference_addr, model_uid=xinference_embedding_model_id
        )
        Chroma.from_documents(
            documents=documents,
            embedding=embedding_function,
            persist_directory=db_addr,
        )
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # finally:
    #     if tmp_save_path_obj.exists():
    #         os.remove(tmp_save_path)


def embedding_all_from_dir():
    texts = process_documents()
    embedding_function = XinferenceEmbeddings(
        server_url=xinference_addr, model_uid=xinference_embedding_model_id
    )
    Chroma.from_documents(texts, embedding_function, persist_directory=db_addr)
