from app.ai.rag.context import build_context
from app.ai.rag.generation import generate_answer
from app.ai.rag.retrieval import retrieve_documents
from app.schemas.rag import RAGResponse, RAGSource


def answer_policy_question(
    question: str,
    temporal_context: str,
) -> RAGResponse:
    """Answer an employee question using HR policy documents."""

    documents = retrieve_documents(
        query=question,
        k=3,
    )

    if not documents:
        return RAGResponse(
            answer=(
                "I couldn't find enough information in the "
                "available HR policies to answer that question."
            ),
            sources=[],
        )

    context = build_context(documents)

    answer = generate_answer(
    question=question,
    context=context,
    temporal_context=temporal_context,
    )

    source_map: dict[tuple[str, int | None], RAGSource] = {}

    for document in documents:
        document_name = document.metadata.get(
            "document_name",
            "Unknown Document",
        )
        page = document.metadata.get("page")

        key = (document_name, page)

        if key not in source_map:
            source_map[key] = RAGSource(
                document=document_name,
                page=page,
            )

    return RAGResponse(
        answer=answer,
        sources=list(source_map.values()),
    )