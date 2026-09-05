from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.chains.ingestion_chain import ingest_video

router = APIRouter(prefix="/api", tags=["ingest"])


class IngestRequest(BaseModel):
    url: str = Field(..., min_length=1)


@router.post("/ingest")
def ingest_endpoint(payload: IngestRequest):
    try:
        result = ingest_video(payload.url)
        return {
            "session_id": result["session_id"],
            "video_id": result["video_id"],
            "title": result["title"],
            "chunk_count": result["chunk_count"],
        }
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
