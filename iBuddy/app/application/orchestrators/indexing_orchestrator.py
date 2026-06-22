from pathlib import Path

from datetime import datetime

from app.application.services.metadata_resolver import (
    MetadataResolver,
)

from app.application.services.hash_service import (
    HashService,
)

from app.infrastructure.registry.document_registry import (
    JsonDocumentRegistry,
)

from app.domain.services.document_loader import (
    DocumentLoader,
)

from app.domain.services.chunking_service import (
    ChunkingService,
)

from app.domain.services.embedding_service import (
    EmbeddingService,
)

from app.domain.repositories.vector_store_repository import (
    VectorStoreRepository,
)


from app.application.dto.document_registry_entry import (
    DocumentRegistryEntry,
)

class IndexingOrchestrator:

    def __init__(
        self,
        metadata_resolver: MetadataResolver,
        hash_service: HashService,
        registry: JsonDocumentRegistry,
        document_loader: DocumentLoader,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_store: VectorStoreRepository,
    ) -> None:

        self._metadata_resolver = (
            metadata_resolver
        )

        self._hash_service = (
            hash_service
        )

        self._registry = registry

        self._document_loader = (
            document_loader
        )

        self._chunking_service = (
            chunking_service
        )

        self._embedding_service = (
            embedding_service
        )

        self._vector_store = (
            vector_store
        )

    def should_index(
            self,
            file_path: str,
    ) -> bool:
        file_hash = (
            self._hash_service
            .generate_file_hash(
                file_path
            )
        )

        return (
            self._registry
            .is_document_changed(
                file_name=Path(
                    file_path
                ).name,
                current_hash=file_hash,
            )
        )

    def index_document(
            self,
            file_path: str,
    ) -> None:

        metadata = (
            self._metadata_resolver.resolve(
                file_path
            )
        )

        print(f"metadata: {metadata}")

        file_hash = (
            self._hash_service
            .generate_file_hash(
                file_path
            )
        )

        print(f"file_hash: {file_hash}")


        file_name = Path(
            file_path
        ).name

        if not self._registry.is_document_changed(
                file_name=file_name,
                current_hash=file_hash,
        ):
            print(
                f"Skipping {file_name}"
            )
            return

        document = (
            self._document_loader.load(
                file_path
            )
        )

        print(f"document: {document.file_name}")

        chunks = (
            self._chunking_service
            .chunk_document(
                document
            )
        )

        embeddings = (
            self._embedding_service
            .embed_texts(
                [
                    chunk.chunk_text
                    for chunk in chunks
                ]
            )
        )

        self._vector_store.add_chunks(
         chunks=chunks,
         embeddings=embeddings)

        entry = (
            DocumentRegistryEntry(
                document_id=document.document_id,
                file_name=file_name,
                file_hash=file_hash,
                department=metadata.department.value,
                category=metadata.category.value,
                indexed_at=datetime.utcnow().isoformat(),
            )
        )

        self._registry.upsert_document(
            entry
        )

    def index_directory(
            self,
            directory_path: str,
    ) -> None:
        """
        Index all PDFs in a directory.
        """

        pdf_directory = Path(
            directory_path
        )

        pdf_files = sorted(
            pdf_directory.glob("*.pdf")
        )

        print(
            f"Found {len(pdf_files)} PDFs"
        )

        for pdf_file in pdf_files:
            print(
                f"\nIndexing: "
                f"{pdf_file.name}"
            )

            self.index_document(
                str(pdf_file)
            )
