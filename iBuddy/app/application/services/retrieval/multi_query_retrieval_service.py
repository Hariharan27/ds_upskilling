from app.application.services.conversational_query_expansion.models import ConversationalQueryExpansionRequest
from app.domain.entities.retrieval_request import RetrievalRequest
from app.domain.entities.search_result import SearchResult
from app.domain.services.conversational_query_expansion_service import  ConversationalQueryExpansionService
from app.application.services.retrieval.retrieval_service import RetrievalService
from app.domain.services.reranking_service import RerankingService


class MultiQueryRetrievalService:

    def __init__(
            self,
            query_expand_service:ConversationalQueryExpansionService,
            retrival_service:RetrievalService,
            reranking_service: RerankingService,
    )->None:
        self.query_expand_service = query_expand_service
        self.retrival_service = retrival_service
        self.reranking_service = reranking_service

    def _rrf_fusion(
            self,
            all_results: list[list[SearchResult]],
    ) -> list[SearchResult]:
        """
        Fuse multiple ranked result lists
        using Reciprocal Rank Fusion.
        """

        RRF_K = 60

        rrf_scores: dict[str, float] = {}

        search_results: dict[str, SearchResult] = {}

        for query_results in all_results:

            for rank, result in enumerate(
                    query_results,
                    start=1,
            ):
                score = 1 / (
                        RRF_K + rank
                )

                rrf_scores[result.chunk_id] = (
                        rrf_scores.get(
                            result.chunk_id,
                            0.0,
                        )
                        + score
                )

                search_results[result.chunk_id] = result

        sorted_chunk_ids = sorted(
            rrf_scores.keys(),
            key=lambda chunk_id: rrf_scores[chunk_id],
            reverse=True,
        )

        return [
            search_results[chunk_id]
            for chunk_id in sorted_chunk_ids
        ]

    def retrieve(
            self,
            request: RetrievalRequest,
    ) -> list[SearchResult]:

        expansion_request = (
            ConversationalQueryExpansionRequest(
                query=request.query,
                conversation_history=request.conversation_history,
            )
        )

        queries = (
            self.query_expand_service.expand(
                expansion_request,
            )
        )

        print(queries)

        all_results: list[list[SearchResult]] = []

        for query in queries:
            retrieval_request = RetrievalRequest(
                query=query,
                top_k=request.top_k,
                similarity_threshold=request.similarity_threshold,
                department=request.department,
                category=request.category,
            )

            query_results = (
                self.retrival_service.retrieve(
                    retrieval_request,
                )
            )

            all_results.append(
                query_results,
            )


        results =  self._rrf_fusion(all_results)

        results = (
            self.reranking_service.rerank(
                query=request.query,
                results=results,
                top_k=request.top_k,
            )
        )
        
        return results

