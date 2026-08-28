from langchain_core.documents import Document

def build_context(documents: list[Document]) -> str:
    """Convert retrieved documents into grounded LLM context."""

    context_parts = []

    for index, document in enumerate(documents,start=1):
        document_name = document.metadata.get(
            "document_name"
            "Unknown Document",
        )
        page = document.metadata.get(
            "page",
            "Unknown Page",
        )

        context_parts.append(
            f"""[Source {index}]
Document: {document_name}
Page: {page}

{document.page_content}
"""
        )

    return "\n\n".join(context_parts)