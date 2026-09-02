from typing import Literal
from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether
from app.core.timing import log_duration
from app.core.langfuse import get_langfuse
from app.core.config import get_settings
from app.core.langfuse import get_langfuse_handler
from app.core.cache import get_cache
from app.ai.graphs.route_decision import RouteDecision
from app.ai.graphs.deterministic_router import deterministic_route

ROUTER_PROMPT_VERSION = "v1"



@lru_cache(maxsize=1)
def get_router():
    """Create the structured LLM router."""

    settings = get_settings()

    llm = ChatTogether(
        model=settings.together_model,
        api_key=settings.together_api_key,
        temperature=0,
    )

    return llm.with_structured_output(RouteDecision)


ROUTER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the routing component of an employee assistant.

Classify the employee's request into exactly one intent.

Intents:

- policy:
  Questions about company policies, rules, eligibility,
  benefits, holidays, reimbursements, leave policy,
  WFH policy, staff loan policy, etc.

- attendance:
  Questions about an employee's attendance, attendance records,
  working days, or attendance status.

- leave:
  Requests or questions about an employee's leave balance,
  leave application, leave status, or leave history.

- wfh:
  Requests to apply for, cancel, or check an employee's
  work-from-home arrangement.

- ticket:
  Requests to create, update, or check an IT/support ticket.

- unknown:
  Anything outside the capabilities above.

Important:
A question about a company policy is "policy" even if it mentions
leave or WFH.

For example:
"How many WFH days are allowed?" → policy
"Can I take WFH tomorrow?" → wfh
"How many leave days am I entitled to?" → policy
"How many leave days do I have left?" → leave
""",
        ),
        ("human", "{message}"),
    ]
)

def route_message(message: str) -> RouteDecision:
    """Classify an employee message."""

    settings = get_settings()
    cache = get_cache()
    langfuse = get_langfuse()

    with langfuse.start_as_current_observation(
        name="router",
        as_type="chain",
        input={"message": message},
    ) as observation:

        # 1. Try deterministic routing first
        deterministic_decision = deterministic_route(message)

        if deterministic_decision:
            observation.update(
                output={
                    "intent": deterministic_decision.intent,
                    "cache": "not_used",
                    "routing_source": "deterministic",
                }
            )

            return deterministic_decision

        # 2. Deterministic routing could not confidently classify.
        #    Try Redis router cache.
        cache_key = cache.make_router_key(
            message=message,
            model=settings.together_model,
            prompt_version=ROUTER_PROMPT_VERSION,
        )

        cached_intent = cache.get(cache_key)

        if cached_intent:
            decision = RouteDecision(intent=cached_intent)

            observation.update(
                output={
                    "intent": decision.intent,
                    "cache": "hit",
                    "routing_source": "cache",
                }
            )

            return decision

        # 3. Cache miss → call router LLM
        router = get_router()
        chain = ROUTER_PROMPT | router

        with log_duration("router"):
            decision = chain.invoke(
                {"message": message},
                config={
                    "callbacks": [get_langfuse_handler()],
                },
            )

        # 4. Cache the LLM routing decision
        cache.set(
            cache_key,
            decision.intent,
        )

        observation.update(
            output={
                "intent": decision.intent,
                "cache": "miss",
                "routing_source": "llm",
            }
        )

        return decision