from langchain_core.documents import Document

from app.ai.rag.vector_store import get_qdrant_vector_store



def retrieve_documents(query: str, top_k: int = 5) -> list[Document]:
    vector_store = get_qdrant_vector_store()
    return vector_store.similarity_search(query, k=top_k)