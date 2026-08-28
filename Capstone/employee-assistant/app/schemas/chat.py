from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    message:str = Field(
        min_length=1,
        description="message sent by the employee."
    )


class ChatResponse(BaseModel):
    message:str