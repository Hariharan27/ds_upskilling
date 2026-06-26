from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# project_root/
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # ChromaDB
    chroma_db_path: str = "chroma_db"
    chroma_collection_name: str = "ibuddy_documents"

    # LLM - Together AI
    together_api_key: str | None = None
    together_model: str = "openai/gpt-oss-20b"

    llm_temperature: float = 0.0
    llm_max_tokens: int = 512
    llm_timeout: int = 30

    # Retry
    max_retries: int = 3
    retry_delay_seconds: int = 2

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    reranker_model: str = "BAAI/bge-reranker-base"


@lru_cache
def get_settings() -> Settings:
    return Settings()