from pydantic import BaseModel


class IntentClassificationResult(BaseModel):
    tool_name: str
    confidence: float
    reason: str