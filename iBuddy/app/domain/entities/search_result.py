from dataclasses import dataclass,field

@dataclass(slots=True)
class SearchResult:
    chunk_id: str
    document_id: str
    file_name: str
    chunk_text: str
    similarity_score: float
    metadata: dict = field(default_factory=dict)