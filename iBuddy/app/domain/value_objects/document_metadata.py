from dataclasses import dataclass

from app.domain.enums.department import (
    Department,
)
from app.domain.enums.document_category import (
    DocumentCategory,
)


@dataclass(frozen=True)
class DocumentMetadata:
    department: Department
    category: DocumentCategory