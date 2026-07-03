from dataclasses import dataclass, field

from app.domain.enums.department import Department
from app.domain.enums.document_category import DocumentCategory
from app.domain.models.chat_message import ChatMessage


@dataclass
class RetrievalRequest:
    query: str
    conversation_history: list[ChatMessage] = field(
        default_factory=list,
    )
    top_k:int = 5
    similarity_threshold: float = 0.45
    department: Department | None = None
    category: DocumentCategory | None = None
