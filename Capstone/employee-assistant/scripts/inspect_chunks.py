from pathlib import Path

from app.ai.rag.ingestion import load_documents
from app.ai.rag.chunking import chunk_documents


DOCUMENTS_DIR = Path("data/documents")

documents = load_documents(DOCUMENTS_DIR)
chunks = chunk_documents(documents)

print(f"Loaded pages : {len(documents)}")
print(f"Created chunks: {len(chunks)}")

for index, chunk in enumerate(chunks[:10]):
    print("\n" + "=" * 80)
    print(f"Chunk: {index}")
    print("Document:", chunk.metadata.get("document_name"))
    print("Page:", chunk.metadata.get("page"))
    print("Characters:", len(chunk.page_content))
    print("Content:")
    print(chunk.page_content)