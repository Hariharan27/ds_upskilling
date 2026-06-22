from dataclasses import dataclass

@dataclass
class DocumentRegistryEntry:
    document_id: str
    file_name: str
    file_hash: str
    department: str
    category: str
    indexed_at: str