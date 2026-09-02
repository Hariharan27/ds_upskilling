import pytest

from app.ai.rag.generation import generate_answer


@pytest.mark.integration
def test_rag_answer_is_grounded_in_policy_context() -> None:
    question = "Can I work from home 12 days a month?"

    context = (
        "Employees may work from home up to 8 days per month. "
        "Requests must follow the organization's WFH policy."
    )

    temporal_context = "Current date: 2026-09-02"

    answer = generate_answer(
        question=question,
        context=context,
        temporal_context=temporal_context,
    )

    answer_lower = answer.lower()

    assert "12 days" not in answer_lower
    assert "8" in answer_lower
    assert "per month" in answer_lower