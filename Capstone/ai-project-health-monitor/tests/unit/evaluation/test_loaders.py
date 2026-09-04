import json

import pytest

from ai_project_health_monitor.domain.models.risk_signal import RiskType
from ai_project_health_monitor.evaluation.loaders import (
    load_risk_evaluation_cases,
)


def test_load_risk_evaluation_cases(tmp_path) -> None:
    dataset = [
        {
            "case_id": "RISK-001",
            "project_id": "PROJ-001",
            "evidence_event_ids": ["EVT-JIRA-001"],
            "expected_risk_types": ["blocker"],
            "expected_severities": ["high"],
        }
    ]

    path = tmp_path / "risk_golden.json"
    path.write_text(
        json.dumps(dataset),
        encoding="utf-8",
    )

    cases = load_risk_evaluation_cases(path)

    assert len(cases) == 1
    assert cases[0].case_id == "RISK-001"
    assert cases[0].project_id == "PROJ-001"
    assert cases[0].evidence_event_ids == ["EVT-JIRA-001"]
    assert cases[0].expected_risk_types == [RiskType.BLOCKER]


def test_load_risk_evaluation_cases_rejects_missing_file(
    tmp_path,
) -> None:
    path = tmp_path / "missing.json"

    with pytest.raises(
        FileNotFoundError,
        match="Risk evaluation dataset not found",
    ):
        load_risk_evaluation_cases(path)


def test_load_risk_evaluation_cases_rejects_non_array(
    tmp_path,
) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(
        json.dumps({"case_id": "RISK-001"}),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="must contain a JSON array",
    ):
        load_risk_evaluation_cases(path)