from app.ai.graphs.deterministic_router import deterministic_route

from tests.evaluation.golden_dataset import (
    GOLDEN_DATASET,
    GOLDEN_DATASET_VERSION,
)


def test_golden_dataset_deterministic_routing() -> None:
    total = len(GOLDEN_DATASET)
    deterministic_matches = 0
    deterministic_correct = 0
    fallback = 0
    incorrect = 0

    print(f"\nGolden dataset: {GOLDEN_DATASET_VERSION}")

    for case in GOLDEN_DATASET:
        decision = deterministic_route(case["question"])

        if decision is None:
            fallback += 1
            continue

        deterministic_matches += 1

        if decision.intent == case["expected_intent"]:
            deterministic_correct += 1
        else:
            incorrect += 1
            print(
                f"\nINCORRECT: {case['id']}"
                f"\nExpected: {case['expected_intent']}"
                f"\nActual: {decision.intent}"
            )

    coverage = deterministic_matches / total if total else 0
    accuracy = (
        deterministic_correct / deterministic_matches
        if deterministic_matches
        else 0
    )

    print(f"\nTotal cases: {total}")
    print(f"Deterministic matches: {deterministic_matches}")
    print(f"LLM fallback: {fallback}")
    print(f"Incorrect deterministic routes: {incorrect}")
    print(f"Deterministic coverage: {coverage:.2%}")
    print(f"Deterministic accuracy: {accuracy:.2%}")

    assert incorrect == 0