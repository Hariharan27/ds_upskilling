from langchain_core.documents import Document

from app.ai.rag.vector_store import get_qdrant_vector_store
from app.core.langfuse import get_langfuse
from app.core.timing import log_duration


DEFAULT_TOP_K = 3
RELEVANCE_THRESHOLD = 0.60


def retrieve_documents(
    query: str,
    k: int = DEFAULT_TOP_K,
) -> list[Document]:
    """Retrieve relevant policy chunks from Qdrant."""

    vector_store = get_qdrant_vector_store()
    langfuse = get_langfuse()

    with langfuse.start_as_current_observation(
        name="retrieval",
        as_type="retriever",
        input={
            "query": query,
            "top_k": k,
        },
    ) as observation:

        with log_duration("retrieving_documents"):
            results = vector_store.similarity_search_with_score(
                query,
                k=k,
            )

        relevant_documents = [
            document
            for document, score in results
            if score >= RELEVANCE_THRESHOLD
        ]

        observation.update(
            output={
                "retrieved_count": len(results),
                "relevant_count": len(relevant_documents),
                "threshold": RELEVANCE_THRESHOLD,
                "documents": [
                    {
                        "document": document.metadata.get(
                            "document_name",
                            "Unknown Document",
                        ),
                        "page": document.metadata.get("page"),
                        "score": score,
                    }
                    for document, score in results
                ],
            }
        )

    return relevant_documents