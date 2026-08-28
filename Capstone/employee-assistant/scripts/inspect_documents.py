from pathlib import Path

from app.ai.rag.ingestion import load_documents

DOCUMENTS_DIR = Path("data/documents")

documents = load_documents(DOCUMENTS_DIR)


print(f"Loaded {len(documents)} pages")


for document in documents:
    print("\n---")
    print("Source:", document.metadata.get("source"))
    print("Page:", document.metadata.get("page"))
    print("Characters:", len(document.page_content))
    print("Preview:", document.page_content[:300].replace("\n", " "))