import pytest

from app.ai.graphs.deterministic_router import deterministic_route


PARAPHRASE_DATASET = [
    ("What's my yearly leave entitlement?", "policy"),
    ("How many days of paid leave do employees get?", "policy"),
    ("Can unused earned leave be carried over?", "policy"),
    ("What happens to unused casual leave?", "policy"),
    ("Please submit leave for tomorrow", "leave"),
    ("I want to apply for leave next Monday", "leave"),
    ("Show me how much leave I have remaining", "leave"),
    ("How often can employees work remotely?", "policy"),
    ("What's the monthly WFH allowance?", "policy"),
    ("Are there limits on working from home?", "policy"),
    ("I'd like to work remotely tomorrow", "wfh"),
    ("Please request WFH for tomorrow", "wfh"),
    ("What should I do with a damaged company laptop?", "policy"),
    ("What are the rules for company IT equipment?", "policy"),
    ("I need to report a technical problem", "ticket"),
    ("Can you create an IT support request?", "ticket"),
    ("Does the company pay for professional certifications?", "policy"),
    ("How much do we get for the marriage benefit?", "policy"),
    ("When is the next company holiday?", "policy"),
    ("How can I redeem my Docker points?", "policy"),
    ("Can employees get a staff loan?", "policy"),
    ("What is the budget for team outings?", "policy"),
    ("Can I take leave?", None),
    ("I want to work from home", None),
    ("I have a laptop problem", None),
]


@pytest.mark.parametrize(
    ("message", "expected_intent"),
    PARAPHRASE_DATASET,
)
def test_deterministic_router_paraphrases(message, expected_intent):
    decision = deterministic_route(message)

    if expected_intent is None:
        assert decision is None
    else:
        assert decision is not None
        assert decision.intent == expected_intent