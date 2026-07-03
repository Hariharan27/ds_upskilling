from app.infrastructure.loaders.pdf_document_loader import (
    PdfDocumentLoader
)
from app.infrastructure.chunkers.recursive_chunking_service import (
    RecursiveChunkingService
)
from  app.infrastructure.embeddings.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService
)
from app.infrastructure.vectorstores.chroma_vector_store_repository import (
    ChromaVectorStoreRepository
)

import os

print(os.getcwd())

def main() -> None:

    loader = PdfDocumentLoader()

    chunking_service = RecursiveChunkingService()

    embedding_service = SentenceTransformerEmbeddingService()

    repository = (
        ChromaVectorStoreRepository()
    )

    pdf_path = (
        "/Users/ideas2it/Documents/"
        "Data Science &Gen AI/"
        "GenAIDataSciencePractice/"
        "iBuddy/data/incoming/"
        "Revised Leave Policy - I2I.pdf"
    )



    document = loader.load(pdf_path)

    print(f"Loading Document",
          f"{document.file_name}")

    chunks = chunking_service.chunk_document(document)

    print(f"Chunking Document",
          f"length: {len(chunks)}")

    embeddings = (
        embedding_service.embed_texts([
            chunk.chunk_text
            for chunk in chunks
        ])
    )

    print(f"Embedding Document",
          f"length: {len(embeddings)}")

    repository.add_chunks(chunks, embeddings)

    print(
        f"Indexed chunks: "
        f"{len(chunks)}"
    )

    print(
        f"Collection count: "
        f"{repository.count()}"
    )



if __name__ == "__main__":
    main()

