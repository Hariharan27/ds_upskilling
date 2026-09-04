import json
from pathlib import Path

from ai_project_health_monitor.evaluation.models.risk import (
    RiskEvaluationCase,
)


def load_risk_evaluation_cases(
    path: Path,
) -> list[RiskEvaluationCase]:
    """Load risk evaluation cases from a JSON file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Risk evaluation dataset not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    if not isinstance(raw_data, list):
        raise ValueError(
            "Risk evaluation dataset must contain a JSON array"
        )

    return [
        RiskEvaluationCase.model_validate(item)
        for item in raw_data
    ]