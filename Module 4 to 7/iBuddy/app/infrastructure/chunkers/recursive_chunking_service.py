from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.domain.entities.chunk import Chunk

from app.domain.entities.document import Document
from app.domain.services.chunking_service import (
    ChunkingService,
)

class RecursiveChunkingService(
    ChunkingService
):
    """
    Recursive chunking implementation.
    """
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> None:
        self._splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        )

    def chunk_document(
        self,
        document: Document,
    ) -> list[Chunk]:

        chunks = self._splitter.split_text(
            document.content
        )

        return [
            Chunk(
                chunk_id=(
                    f"{document.document_id}"
                    f"_chunk_{index}"
                ),
                document_id=document.document_id,
                chunk_text=chunk_text,
                chunk_index=index,
                file_name=document.file_name,
                metadata=document.metadata,
            )
            for index, chunk_text in enumerate(chunks)
        ]