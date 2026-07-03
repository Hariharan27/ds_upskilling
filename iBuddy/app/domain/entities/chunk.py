from dataclasses import dataclass,field

@dataclass(slots=True)
class Chunk:
    """
    Represents a searchable chunk
    generated from a document.
    """
    chunk_id: str
    document_id: str
    chunk_text: str
    chunk_index: int
    file_name: str
    metadata: dict = field(default_factory=dict)