from app.ai.graphs.deterministic_router import deterministic_route
from tests.evaluation.routing_dataset import ROUTING_EVALUATION_DATASET
from tests.evaluation.test_deterministic_router_paraphrases import PARAPHRASE_DATASET


def test_deterministic_routing_coverage():
    dataset = ROUTING_EVALUATION_DATASET + PARAPHRASE_DATASET

    total = len(dataset)
    deterministic_matches = 0
    fallback = 0

    for message, _ in dataset:
        decision = deterministic_route(message)

        if decision is None:
            fallback += 1
        else:
            deterministic_matches += 1

    coverage = deterministic_matches / total * 100

    print(f"\nTotal requests: {total}")
    print(f"Deterministic matches: {deterministic_matches}")
    print(f"LLM fallback: {fallback}")
    print(f"Deterministic coverage: {coverage:.2f}%")

    assert total > 0