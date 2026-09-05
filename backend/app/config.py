from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "youtube-rag"
    app_env: str = "development"
    llm_provider: str = "google"
    llm_model: str = "gemini-3.6-flash"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    backend_cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    chroma_persist_directory: str = str(BASE_DIR / "chroma_store")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
