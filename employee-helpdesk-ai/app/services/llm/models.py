from pydantic import BaseModel
from app.schemas.response import UsageResponse

class LLMResponse(BaseModel):

    content: str

    model: str

    usage: UsageResponse