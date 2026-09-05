from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.config import settings
from app.services.vector_store import build_session_store
from app.services.youtube import extract_video_id, fetch_transcript_text

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def ingest_video(url: str) -> dict[str, Any]:
    video_id = extract_video_id(url)
    transcript_text, title = fetch_transcript_text(video_id, languages=["en"])

    if not transcript_text or not transcript_text.strip():
        raise ValueError("No transcript content was found for this video.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_text(transcript_text)

    documents = [
        Document(
            page_content=chunk,
            metadata={
                "source_url": url,
                "title": title or video_id,
                "video_id": video_id,
                "chunk_index": idx,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        for idx, chunk in enumerate(chunks)
    ]

    session_id = str(uuid4())
    build_session_store(session_id, settings.chroma_persist_directory, documents)

    return {
        "session_id": session_id,
        "video_id": video_id,
        "title": title or video_id,
        "chunk_count": len(documents),
        "source_url": url,
    }
