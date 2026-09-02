import pytest

from app.ai.graphs.deterministic_router import deterministic_route
from tests.evaluation.routing_dataset import ROUTING_EVALUATION_DATASET


@pytest.mark.parametrize(
    ("message", "expected_intent"),
    ROUTING_EVALUATION_DATASET,
)
def test_deterministic_router(message, expected_intent):
    decision = deterministic_route(message)

    if expected_intent is None:
        assert decision is None
    else:
        assert decision is not None
        assert decision.intent == expected_intent