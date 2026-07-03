from sentence_transformers import CrossEncoder

from app.domain.entities.search_result import SearchResult
from app.domain.services.reranking_service import (
    RerankingService,
)
from app.shared.config import (
    get_settings,
)

settings = get_settings()

class BGERerankingService(
    RerankingService,
):

    def __init__(
        self,
        model_name: str = settings.reranker_model,
    ) -> None:

        self._model = CrossEncoder(
            model_name,
        )

    def rerank(
            self,
            query: str,
            results: list[SearchResult],
            top_k: int,
    ) -> list[SearchResult]:

        pairs = [
            (
            query,
            result.chunk_text
            )
            for result in results
        ]

        scores = self._model.predict(pairs)

        score_results = list(zip(scores, results))

        score_results.sort(key=lambda x: x[0], reverse=True)

        return [
            result
            for _,result in score_results[:top_k]
        ]


