from chromadb import PersistentClient

from app.domain.entities.chunk import Chunk

from app.domain.repositories.vector_store_repository import (
    VectorStoreRepository,
)

from app.domain.entities.search_result import (
    SearchResult,
)
from app.shared.config import get_settings



class ChromaVectorStoreRepository(
    VectorStoreRepository
):
    """
    ChromaDB implementation of
    VectorStoreRepository.
    """
    def __init__(
        self,
        db_path: str|None = None,
    ) -> None:

        settings = get_settings()

        self._client = PersistentClient(
            path= ( db_path or settings.chroma_db_path),
        )

        self._collection = (
            self._client.get_or_create_collection(
                name= settings.chroma_collection_name,
                metadata={
                    "hnsw:space": "cosine",
                },
            )
        )

    def add_chunks(
            self,
            chunks: list[Chunk],
            embeddings: list[list[float]],
    ) -> None:
        """
        Store chunks and embeddings.
        """

        self._collection.add(
            ids=[
                chunk.chunk_id
                for chunk in chunks
            ],
            documents=[
                chunk.chunk_text
                for chunk in chunks
            ],
            embeddings=embeddings,
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "file_name": chunk.file_name,
                    "chunk_index": chunk.chunk_index,
                    "department":  chunk.metadata["department"],
                    "category": chunk.metadata["category"],
                }
                for chunk in chunks
            ],
        )

    def search(
            self,
            query_embedding: list[float],
            top_k: int = 5,
            metadata_filter: dict[str, str] | None = None,
    ) -> list[SearchResult]:
        """
        Search similar chunks.
        """

        response = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where = metadata_filter
        )

        results = []

        ids = response["ids"][0]
        documents = response["documents"][0]
        metadatas = response["metadatas"][0]
        distances = response["distances"][0]

        for (
                chunk_id,
                document,
                metadata,
                distance,
        ) in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            results.append(
                SearchResult(
                    chunk_id=chunk_id,
                    document_id= str(metadata.get("document_id","")),
                    file_name= str(metadata.get("file_name", "")),
                    chunk_text= document,
                    similarity_score= 1 - distance,
                    metadata= dict(metadata),
                )
            )

        return results

    def delete_by_document_id(
            self,
            document_id: str,
    ) -> None:
        """
        Delete all chunks belonging to a document.
        """

        self._collection.delete(
            where= {
                "document_id": document_id,
            }
        )

    def count(self) -> int:
        """
        Return total vectors stored.
        """
        return self._collection.count()

