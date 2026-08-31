from langchain_core.documents import Document

from app.ai.rag.vector_store import get_qdrant_vector_store


DEFAULT_TOP_K = 3
RELEVANCE_THRESHOLD = 0.60


def retrieve_documents(
    query: str,
    k: int = DEFAULT_TOP_K,
) -> list[Document]:
    """Retrieve relevant policy chunks from Qdrant."""

    vector_store = get_qdrant_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    relevant_documents = [
        document
        for document, score in results
        if score >= RELEVANCE_THRESHOLD
    ]

    return relevant_documents