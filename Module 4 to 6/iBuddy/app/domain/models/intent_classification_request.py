from pydantic import BaseModel
from pydantic import Field

from app.domain.models.chat_message import ChatMessage

class IntentClassificationRequest(BaseModel):
    query: str
    conversation_history: list[ChatMessage] = Field(
        default_factory=list,
    )