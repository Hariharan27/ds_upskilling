from app.domain.entities.retrieval_request import RetrievalRequest
from app.domain.entities.search_result import SearchResult
from app.domain.services.query_expansion_service import  QueryExpansionService
from app.application.services.retrieval.retrieval_service import RetrievalService


def _rrf_fusion(
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


class MultiQueryRetrievalService:

    def __init__(
            self,
            query_expand_service:QueryExpansionService,
            retrival_service:RetrievalService,
    )->None:
        self.query_expand_service = query_expand_service
        self.retrival_service = retrival_service

    def retrieve(
            self,
            request: RetrievalRequest,
    ) -> list[SearchResult]:

        queries = (
            self.query_expand_service
            .expand(request.query)
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


        return _rrf_fusion(all_results)

