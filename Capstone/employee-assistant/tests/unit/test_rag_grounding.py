from app.ai.prompts.rag import RAG_PROMPT


def test_rag_prompt_requires_context_grounding() -> None:
    prompt = RAG_PROMPT.format(
        question="Can I work from home 12 days a month?",
        context="Employees may work from home up to 8 days per month.",
        temporal_context="Current date: 2026-09-02",
    )

    assert "Answer employee questions using ONLY the provided HR policy context." in prompt
    assert "Do not invent or assume policy information." in prompt
    assert "If the context does not contain enough information to answer" in prompt


def test_rag_prompt_separates_temporal_context_from_policy() -> None:
    prompt = RAG_PROMPT.format(
        question="Can I apply leave tomorrow?",
        context="Employees must apply for leave through the HR system.",
        temporal_context="Current date: 2026-09-02",
    )

    assert "Current date: 2026-09-02" in prompt
    assert "Employees must apply for leave through the HR system." in prompt
    assert "The current date and time provide temporal context only" in prompt
    assert "provide or override HR policy information." in prompt