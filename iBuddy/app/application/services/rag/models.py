from pydantic import BaseModel


class RAGPromptRequest(BaseModel):
    query: str
    context: str

class RAGResponse(BaseModel):
    answer: str
    sources: list[str]
    input_tokens: int
    output_tokens: int
    total_tokens: int