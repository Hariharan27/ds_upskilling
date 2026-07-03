class LLMClientError(Exception):
    """
    Base exception for LLM client failures.
    """


class LLMResponseError(LLMClientError):
    """
    Raised when the LLM returns
    an invalid or empty response.
    """