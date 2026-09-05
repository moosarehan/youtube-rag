from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from app.services.vector_store import get_session_collection
from app.config import settings


def get_session_retriever(session_id: str):
    vector_store = get_session_collection(session_id, settings.chroma_persist_directory)
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "lambda_mult": 0.5,
        }
    )


def format_docs(docs: list[Document]) -> str:
    formatted = []
    for doc in docs:
        formatted.append(doc.page_content)
    return "\n\n".join(formatted)


def get_source_docs(docs: list[Document]) -> list[dict[str, str]]:
    sources = []
    for doc in docs:
        meta = doc.metadata or {}
        sources.append(
            {
                "url": meta.get("source_url") or "unknown",
                "snippet": (doc.page_content[:220] + "...") if len(doc.page_content) > 220 else doc.page_content,
                "title": meta.get("title") or "unknown",
            }
        )
    return sources
