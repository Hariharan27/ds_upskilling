from dataclasses import dataclass

@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int
    output_tokens: int
    total_tokens: int