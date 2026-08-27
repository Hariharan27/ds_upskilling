from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document



def load_pdf(path:Path) -> list[Document]:
    """Load a single PDF into LangChain Documents.""" 
    loader = PyMuPDFLoader(str(path))
    documents = loader.load()

    for document in documents:
        document.metadata.update(
            {
                "document_name": path.stem,
                "document_type": "policy",
                "source": str(path),
            }
        )
    
    return documents

def load_documents(directory:Path) -> list[Document]:
    """Load all PDFs in a directory into LangChain Documents."""
    documents = []
    for path in directory.glob("*.pdf"):
        documents.extend(load_pdf(path))
    return documents