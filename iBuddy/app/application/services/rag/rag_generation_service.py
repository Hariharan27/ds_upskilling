from app.application.services.rag.models import (
    RAGPromptRequest,
    RAGResponse,
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
        request: RAGPromptRequest,
    ) -> RAGResponse:

        retrieval_request = RetrievalRequest(
            query=request.query,
        )

        results = (
            self._retrieval_service.retrieve(
                retrieval_request,
            )
        )

        context = (
            self._context_builder.build(
                results,
            )
        )

        prompt_request = RAGPromptRequest(
            query=request.query,
            context=context,
        )

        llm_request = (
            self._prompt_builder.build(
                prompt_request,
            )
        )

        llm_response = (
            self._llm_client.generate_text(
                llm_request,
            )
        )

        sources = sorted(
            {
                result.file_name
                for result in results
            }
        )

        return RAGResponse(
            answer=llm_response.content,
            sources=sources,
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
            total_tokens=llm_response.total_tokens,
        )