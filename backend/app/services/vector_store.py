from pathlib import Path
from typing import Any

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def get_session_collection(session_id: str, persist_directory: str):
    collection_path = Path(persist_directory) / session_id
    return Chroma(
        collection_name=f"youtube_session_{session_id}",
        embedding_function=get_embeddings(),
        persist_directory=str(collection_path),
    )


def build_session_store(session_id: str, persist_directory: str, docs: list[Any]):
    vector_store = get_session_collection(session_id, persist_directory)
    vector_store.add_documents(docs)
    return vector_store
