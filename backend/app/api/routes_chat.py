from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.chains.rag_chain import build_rag_chain
from app.config import settings

router = APIRouter(prefix="/api", tags=["chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    history: list[ChatMessage] | None = None


@router.post("/chat")
def chat_endpoint(payload: ChatRequest):
    session_dir = Path(settings.chroma_persist_directory) / payload.session_id
    if not session_dir.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    try:
        chain = build_rag_chain(payload.session_id)
        history = [{"role": item.role, "content": item.content} for item in (payload.history or [])]
        result = chain(payload.question, history)
        return {"answer": result["answer"], "sources": result["sources"]}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
