from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):

    APP_NAME: str = "Employee Helpdesk AI"
    APP_VERSION: str = "1.0.0"

    TOGETHER_API_KEY: str = Field(
        min_length=10
    )
    MODEL_NAME: str = (
        "openai/gpt-oss-20b"
    )

    TEMPERATURE: float = 0.2

    MAX_TOKENS: int = 300

    REQUEST_TIMEOUT: int = 30

    MAX_RETRIES: int = 3

    RETRY_DELAY_SECONDS: int = 2

    class Config:
        env_file = "app/.env"


settings = Settings()