from enum import StrEnum
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Supported application environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    app_name: str = Field(
        default="AI Project Health Monitor",
        min_length=1,
    )
    app_version: str = Field(
        default="0.1.0",
        min_length=1,
    )
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False

@lru_cache
def get_settings() -> Settings:
    return Settings()