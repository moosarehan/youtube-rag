import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

VIDEO_ID_PATTERN = re.compile(
    r"(?:v=|be/|embed/|shorts/)([A-Za-z0-9_-]{11})(?:[?&/]|$)"
)


def extract_video_id(url: str) -> str:
    if not url or not isinstance(url, str):
        raise ValueError("A valid YouTube URL is required.")

    cleaned = url.strip()
    patterns = [
        r"(?:youtube\.com/watch\?.*?v=|youtube\.com/embed/|youtube\.com/shorts/|youtu\.be/)([A-Za-z0-9_-]{11})(?:[?&/]|$)",
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com/watch\?.*?v=([A-Za-z0-9_-]{11})(?:&|$)",
        r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([A-Za-z0-9_-]{11})(?:\?|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, cleaned, re.IGNORECASE)
        if match:
            return match.group(1)

    match = VIDEO_ID_PATTERN.search(cleaned)
    if match:
        return match.group(1)

    raise ValueError("Could not parse a valid YouTube video ID from the provided URL.")


def fetch_transcript_text(video_id: str, languages: list[str] | None = None) -> tuple[str, str | None]:
    transcript_api = YouTubeTranscriptApi()
    try:
        transcript = transcript_api.fetch(video_id, languages=languages or ["en"])
    except TranscriptsDisabled:
        raise TranscriptsDisabled(
            f"Captions are disabled for video {video_id}."
        )
    except NoTranscriptFound:
        try:
            transcript = transcript_api.fetch(video_id)
        except Exception as exc:  # pragma: no cover - re-raise below
            raise exc
    except VideoUnavailable:
        raise VideoUnavailable(f"Video {video_id} is unavailable or private.")

    transcript_list = transcript.to_raw_data()
    text = " ".join(chunk["text"] for chunk in transcript_list)
    title = getattr(transcript, "video_title", None) or None

    return text, title
