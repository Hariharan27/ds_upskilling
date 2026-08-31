from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether
from pydantic import BaseModel, Field

from app.core.config import get_settings


class RouteDecision(BaseModel):
    """Structured routing decision for the employee assistant."""

    intent: Literal[
        "policy",
        "attendance",
        "leave",
        "wfh",
        "ticket",
        "unknown",
    ] = Field(
        description="The capability that should handle the employee request."
    )


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

    router = get_router()

    chain = ROUTER_PROMPT | router

    return chain.invoke(
        {
            "message": message,
        }
    )