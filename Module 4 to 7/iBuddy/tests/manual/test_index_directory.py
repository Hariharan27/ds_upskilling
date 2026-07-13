from app.application.orchestrators.indexing_orchestrator import (
    IndexingOrchestrator,
)

from app.application.services.hash_service import (
    HashService,
)

from app.application.services.metadata_resolver import (
    MetadataResolver,
)

from app.infrastructure.chunkers.recursive_chunking_service import (
    RecursiveChunkingService,
)

from app.infrastructure.embeddings.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
)

from app.infrastructure.loaders.pdf_document_loader import (
    PdfDocumentLoader,
)

from app.infrastructure.registry.document_registry import (
    JsonDocumentRegistry,
)

from app.infrastructure.vectorstores.chroma_vector_store_repository import (
    ChromaVectorStoreRepository,
)


def main() -> None:

    orchestrator = IndexingOrchestrator(
        metadata_resolver=MetadataResolver(),
        hash_service=HashService(),
        registry=JsonDocumentRegistry(),
        document_loader=PdfDocumentLoader(),
        chunking_service=RecursiveChunkingService(),
        embedding_service=(
            SentenceTransformerEmbeddingService()
        ),
        vector_store=(
            ChromaVectorStoreRepository()
        ),
    )

    orchestrator.index_directory(
        "/Users/ideas2it/Documents/Data Science &Gen AI/GenAIDataSciencePractice/Module 4 to 6/iBuddy/data/incoming"
    )


if __name__ == "__main__":
    main()