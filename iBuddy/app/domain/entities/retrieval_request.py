from dataclasses import dataclass

from app.domain.enums.department import Department
from app.domain.enums.document_category import DocumentCategory


@dataclass
class RetrievalRequest:
    query: str
    top_k:int = 5
    similarity_threshold: float = 0.45
    department: Department | None = None
    category: DocumentCategory | None = None
