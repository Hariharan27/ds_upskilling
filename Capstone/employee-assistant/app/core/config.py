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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()