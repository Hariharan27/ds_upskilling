from langchain_core.output_parsers import StrOutputParser
from app.ai.guardrails.pii import redact_pii

from app.ai.models.chat import get_chat_model
from app.ai.prompts.rag import RAG_PROMPT
from app.core.langfuse import get_langfuse
from app.core.timing import log_duration
from app.core.langfuse import get_langfuse_handler
from app.core.cache import get_cache
from app.ai.prompts.rag import RAG_PROMPT_VERSION
from app.core.config import get_settings

def generate_answer(
    question: str,
    context: str,
    temporal_context: str,
) -> str:
    """Generate a grounded answer from retrieved policy context."""

    settings = get_settings()
    cache = get_cache()
    langfuse = get_langfuse()

    cache_key = cache.make_policy_key(
        question=question,
        model=settings.together_model,
        prompt_version=RAG_PROMPT_VERSION,
        temporal_context=temporal_context,
    )

    with langfuse.start_as_current_observation(
        name="generation",
        as_type="chain",
        input={
            "question": redact_pii(question),
        },
    ) as observation:

        cached_answer = cache.get(cache_key)

        if cached_answer is not None:
            observation.update(
                output={
                    "answer": redact_pii(cached_answer),
                    "cache": "hit",
                }
            )

            return cached_answer

        model = get_chat_model()

        chain = RAG_PROMPT | model | StrOutputParser()

        with log_duration("generation"):
            answer = chain.invoke(
                {
                    "context": context,
                    "question": question,
                    "temporal_context": temporal_context,
                },
                config={
                    "callbacks": [get_langfuse_handler()],
                },
            )

        cache.set(
            cache_key,
            answer,
        )

        observation.update(
            output={
                "answer": redact_pii(answer),
                "cache": "miss",
            }
        )

        return answer