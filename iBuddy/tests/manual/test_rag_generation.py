from app.application.services.context_builder.default_context_builder import (
    DefaultContextBuilder,
)
from app.application.services.query_expansion.llm_query_expansion_service import (
    LlmQueryExpansionService,
)
from app.application.services.rag.models import (
    RAGPromptRequest,
)
from app.application.services.rag.prompt_builder import (
    PromptBuilder,
)
from app.application.services.rag.rag_generation_service import (
    RAGGenerationService,
)
from app.application.services.retrieval.multi_query_retrieval_service import (
    MultiQueryRetrievalService,
)
from app.application.services.retrieval.retrieval_service import (
    RetrievalService,
)
from app.infrastructure.embeddings.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
)
from app.infrastructure.llm.together_llm_client import (
    TogetherLLMClient,
)
from app.infrastructure.reranking.bge_reranking_service import (
    BGERerankingService,
)
from app.infrastructure.vectorstores.chroma_vector_store_repository import (
    ChromaVectorStoreRepository,
)


def main() -> None:

    embedding_service = (
        SentenceTransformerEmbeddingService()
    )

    vector_repository = (
        ChromaVectorStoreRepository()
    )

    retrieval_service = (
        RetrievalService(
            embedding_service=embedding_service,
            vector_repository=vector_repository,
        )
    )

    llm_client = TogetherLLMClient()

    query_expansion_service = (
        LlmQueryExpansionService(
            llm_client=llm_client,
        )
    )

    reranking_service = (
        BGERerankingService()
    )

    multi_query_retrieval_service = (
        MultiQueryRetrievalService(
            query_expand_service=query_expansion_service,
            retrival_service=retrieval_service,
            reranking_service=reranking_service,
        )
    )

    context_builder = (
        DefaultContextBuilder()
    )

    prompt_builder = (
        PromptBuilder()
    )

    rag_service = (
        RAGGenerationService(
            retrieval_service=multi_query_retrieval_service,
            context_builder=context_builder,
            prompt_builder=prompt_builder,
            llm_client=llm_client,
        )
    )

    request = RAGPromptRequest(
        query="How many days a new father get a leave?",
        context="",
    )

    response = rag_service.generate(
        request,
    )

    print("\nAnswer")
    print("=" * 80)
    print(response.answer)

    print("\nSources")
    print("=" * 80)

    for source in response.sources:
        print(source)

    print("\nToken Usage")
    print("=" * 80)
    print(f"Input : {response.input_tokens}")
    print(f"Output: {response.output_tokens}")
    print(f"Total : {response.total_tokens}")


if __name__ == "__main__":
    main()