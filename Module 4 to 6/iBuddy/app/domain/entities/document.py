from dataclasses import dataclass,field

@dataclass(slots=True)
class Document:
    """
    Represents a parsed document
    before chunking begins.
    """
    document_id: str
    file_name: str
    file_path: str
    content: str
    metadata: dict = field(default_factory=dict)