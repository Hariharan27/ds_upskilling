from dataclasses import dataclass

@dataclass(frozen=True)
class LLMRequest:
    system_prompt: str
    user_prompt: str
    temperature: float = 0.0
    max_tokens: int = 512