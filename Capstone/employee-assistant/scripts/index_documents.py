from pathlib import Path

from app.ai.rag.vector_store import get_qdrant_vector_store
from app.ai.rag.chunking import chunk_documents
from app.ai.rag.ingestion import load_documents

DOCUMENTS_DIR = Path("data/documents")

def main() -> None:
    documents = load_documents(DOCUMENTS_DIR)
    chunks = chunk_documents(documents)

    print(f"Loaded pages: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    vector_store = get_qdrant_vector_store()
    vector_store.add_documents(chunks)

if __name__ == "__main__":
    main()