from typing import Literal
from typing_extensions import TypedDict
from app.schemas.rag import RAGSource

Intent = Literal[
        "policy",
        "attendance",
        "leave",
        "wfh",
        "ticket",
        "unknown",
]

class EmployeeAssistantState(TypedDict, total=False):
    message:str
    intent: Intent
    response: str
    sources: list[RAGSource]
    temporal_context: str