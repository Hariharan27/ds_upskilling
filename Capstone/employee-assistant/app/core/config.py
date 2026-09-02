from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Employee Assistant API"
    app_version: str = "0.1.0"
    environment: str = "development"
    description: str = "API for assisting employees with various tasks."
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "employee_policies"

    together_api_key: str
    together_model: str
    langfuse_secret_key: str
    langfuse_public_key: str
    langfuse_base_url: str
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()