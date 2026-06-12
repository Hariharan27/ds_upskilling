class LLMServiceError(Exception):
    pass


class LLMTimeoutError(Exception):
    pass


class LLMResponseError(Exception):
    pass

class LLMProviderError(Exception):
    pass


class EmptyLLMResponseError(LLMProviderError):
    pass

class PromptInjectionError(Exception):
    pass