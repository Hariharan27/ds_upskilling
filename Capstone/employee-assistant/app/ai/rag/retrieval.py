from langchain_core.documents import Document

from app.ai.rag.vector_store import get_qdrant_vector_store
from app.ai.rag.reranking import rerank_documents


def retrieve_documents(
    query: str,
    k: int = 10,
    top_n: int = 3,
) -> list[Document]:
    """Retrieve candidates from Qdrant and rerank them."""

    vector_store = get_qdrant_vector_store()

    candidates = vector_store.similarity_search(
        query,
        k=k,
    )

    return rerank_documents(
        query=query,
        documents=candidates,
        top_n=top_n,
    )