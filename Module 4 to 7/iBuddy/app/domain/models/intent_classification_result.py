from pydantic import BaseModel


class IntentClassificationResult(BaseModel):
    tool_name: str | None
    confidence: float
    reason: str