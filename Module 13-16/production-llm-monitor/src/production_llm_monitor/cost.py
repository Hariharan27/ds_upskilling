MODEL_PRICING = {
    "openai/gpt-oss-20b": {
        "input_per_million": 0.05,
        "output_per_million": 0.20,
    }
}


def calculate_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    """Estimate the cost of an LLM request."""

    pricing = MODEL_PRICING.get(model)

    if pricing is None:
        return 0.0

    input_cost = (
        prompt_tokens
        / 1_000_000
        * pricing["input_per_million"]
    )

    output_cost = (
        completion_tokens
        / 1_000_000
        * pricing["output_per_million"]
    )

    return round(input_cost + output_cost, 8)