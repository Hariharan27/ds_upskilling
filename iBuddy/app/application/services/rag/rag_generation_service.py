import time

from app.application.services.rag.models import (
    RAGPromptRequest,
    RAGResponse,
    RAGRequest,
)
from app.application.services.rag.prompt_builder import (
    PromptBuilder,
)
from app.application.services.retrieval.multi_query_retrieval_service import (
    MultiQueryRetrievalService,
)
from app.domain.entities.retrieval_request import (
    RetrievalRequest,
)
from app.domain.services.context_builder import (
    ContextBuilder,
)
from app.domain.services.llm_client import (
    LLMClient,
)


class RAGGenerationService:

    def __init__(
        self,
        retrieval_service: MultiQueryRetrievalService,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ) -> None:

        self._retrieval_service = retrieval_service
        self._context_builder = context_builder
        self._prompt_builder = prompt_builder
        self._llm_client = llm_client

    def generate(
        self,
        request: RAGRequest,
    ) -> RAGResponse:

        overall_start = time.perf_counter()

        retrieval_request = RetrievalRequest(
            query=request.query,
        )

        start = time.perf_counter()

        results = (
            self._retrieval_service.retrieve(
                retrieval_request,
            )
        )

        print(
            f"[Timing] Retrieval       : "
            f"{time.perf_counter() - start:.3f}s"
        )

        start = time.perf_counter()

        context = (
            self._context_builder.build(
                results,
            )
        )

        print(
            f"[Timing] Context Builder : "
            f"{time.perf_counter() - start:.3f}s"
        )

        prompt_request = RAGPromptRequest(
            query=request.query,
            context=context,
        )

        start = time.perf_counter()

        llm_request = (
            self._prompt_builder.build(
                prompt_request,
            )
        )

        print(
            f"[Timing] Prompt Builder  : "
            f"{time.perf_counter() - start:.3f}s"
        )

        start = time.perf_counter()

        llm_response = (
            self._llm_client.generate_text(
                llm_request,
            )
        )

        print(
            f"[Timing] LLM Generation  : "
            f"{time.perf_counter() - start:.3f}s"
        )

        sources = sorted(
            {
                result.file_name
                for result in results
            }
        )

        print(
            f"[Timing] Total Pipeline  : "
            f"{time.perf_counter() - overall_start:.3f}s"
        )

        return RAGResponse(
            answer=llm_response.content,
            sources=sources,
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
            total_tokens=llm_response.total_tokens,
        )