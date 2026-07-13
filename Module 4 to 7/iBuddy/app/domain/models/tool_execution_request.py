from pydantic import BaseModel,Field

from app.domain.models.chat_message import ChatMessage


class ToolExecutionRequest(BaseModel):
    query:str
    conversation_history:list[ChatMessage] = Field(default_factory=list)
    arguments: BaseModel | None = None