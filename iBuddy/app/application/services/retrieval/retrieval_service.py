from app.domain.entities.search_result import SearchResult
from app.domain.repositories.vector_store_repository import VectorStoreRepository
from app.domain.services.embedding_service import EmbeddingService
from app.domain.entities.retrieval_request import RetrievalRequest

class RetrievalService:
    """
    Contract for retrieving embeddings
    """
    def __init__(self,
                 embedding_service: EmbeddingService,
                 vector_repository: VectorStoreRepository,):
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository


    def retrieve(
            self,
            request:RetrievalRequest,
    ) -> list[SearchResult]:
        query_embeddings = (
            self.embedding_service.embed_text(
                request.query
            )
        )
        metadata_filter: dict[str, str] = {}

        if request.department:
            metadata_filter["department"] = request.department

        if request.category:
            metadata_filter["category"] = request.category

        results = (self.vector_repository
                   .search(query_embeddings,
                           request.top_k,
                           metadata_filter= (metadata_filter or None),
                    ))
        return [
            result
            for result in results
            if result.similarity_score >= request.similarity_threshold
        ]

