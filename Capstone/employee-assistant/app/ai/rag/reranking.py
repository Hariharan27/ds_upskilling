from langchain_core.documents import Document
from langchain_community.document_compressors import FlashrankRerank

def rerank_documents(query: str, documents: list[Document], top_n: int = 3) -> list[Document]:
    reranker = FlashrankRerank(top_n = top_n)
    compressed_documents = reranker.compress_documents(documents=documents,query=query)
    return compressed_documents