from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    input_tokens: int
    output_tokens: int
    total_tokens: int