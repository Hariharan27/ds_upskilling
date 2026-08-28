from app.ai.rag.context import build_context
from app.ai.rag.generation import generate_answer
from app.ai.rag.retrieval import retrieve_documents


def answer_policy_question(question: str) -> str:
    """Answer an employee question using HR policy documents."""

    documents = retrieve_documents(
        query=question,
        k=10,
        top_n=3,
    )

    context = build_context(documents)

    return generate_answer(
        question=question,
        context=context,
    )