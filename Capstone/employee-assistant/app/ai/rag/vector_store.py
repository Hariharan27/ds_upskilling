from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.ai.rag.embeddings import get_embedding_model
from app.core.config import get_settings


VECTOR_SIZE = 384


def get_qdrant_client() -> QdrantClient:
    settings = get_settings()

    return QdrantClient(url=settings.qdrant_url)


def ensure_collection() -> None:
    settings = get_settings()
    client = get_qdrant_client()

    collections = client.get_collections()

    existing_names = {
        collection.name
        for collection in collections.collections
    }

    if settings.qdrant_collection not in existing_names:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def get_qdrant_vector_store() -> QdrantVectorStore:
    settings = get_settings()

    ensure_collection()

    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=settings.qdrant_collection,
        embedding=get_embedding_model(),
    )