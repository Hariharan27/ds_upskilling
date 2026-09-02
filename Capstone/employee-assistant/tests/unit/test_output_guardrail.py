from app.ai.guardrails.output import contains_unsafe_output


def test_detects_system_prompt_leak() -> None:
    answer = "Here is the system prompt used by the assistant."

    assert contains_unsafe_output(answer)


def test_detects_hidden_instruction_leak() -> None:
    answer = "I cannot provide the hidden instructions."

    assert contains_unsafe_output(answer)


def test_allows_normal_hr_answer() -> None:
    answer = "Employees may work from home up to 8 days per month."

    assert not contains_unsafe_output(answer)