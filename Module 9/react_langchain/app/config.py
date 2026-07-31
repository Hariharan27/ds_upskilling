import os

from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr

load_dotenv()


class Settings(BaseModel):
    together_api_key: SecretStr
    together_model: str = "openai/gpt-oss-20b"
    temperature: float = 0.0


def get_settings() -> Settings:
    api_key = os.getenv(
        "TOGETHER_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "TOGETHER_API_KEY is not configured."
        )

    return Settings(
        together_api_key=SecretStr(api_key),
    )