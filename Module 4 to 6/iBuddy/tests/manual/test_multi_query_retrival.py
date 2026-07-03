from app.application.services.conversational_query_expansion.llm_conversational_query_expansion_service import LlmConversationalQueryExpansionService
from app.application.services.retrieval.retrieval_service import RetrievalService
from app.application.services.retrieval.multi_query_retrieval_service import MultiQueryRetrievalService
from app.domain.entities.retrieval_request import RetrievalRequest
from app.infrastructure.embeddings.sentence_transformer_embedding_service import SentenceTransformerEmbeddingService
from app.infrastructure.llm.together_llm_client import TogetherLLMClient
from app.infrastructure.vectorstores.chroma_vector_store_repository import ChromaVectorStoreRepository
from app.infrastructure.reranking.bge_reranking_service import  BGERerankingService

def main() -> None:

    embedding_service = (
        SentenceTransformerEmbeddingService()
    )

    vector_repository = (
        ChromaVectorStoreRepository()
    )

    retrieval_service = (
        RetrievalService(embedding_service, vector_repository)
    )

    llm_client = TogetherLLMClient()

    reranking_service = BGERerankingService()

    query_expansion_service = LlmConversationalQueryExpansionService(llm_client)

    multi_query_retrieval_service = (
        MultiQueryRetrievalService(query_expansion_service,retrieval_service,reranking_service)
    )

    request = RetrievalRequest(
        query="How many WFH days are allowed?",
        top_k=5,
        similarity_threshold=0.40,
    )

    results = multi_query_retrieval_service.retrieve(request)

    for rank, result in enumerate(results, start=1):

        print(
            f"Rank={rank} | "
            f"Similarity={result.similarity_score:.3f}"
        )

        print(
            f"Chunk={result.chunk_id}"
        )

        print(
            f"File={result.file_name}"
        )

        print(
            result.chunk_text
        )

        print()



if __name__ == "__main__":
    main()









