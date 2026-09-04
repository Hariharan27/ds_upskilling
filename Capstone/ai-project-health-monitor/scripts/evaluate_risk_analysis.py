from pathlib import Path

from ai_project_health_monitor.analysis.llm_factory import LLMClientFactory
from ai_project_health_monitor.analysis.llm_risk_analyzer import LLMRiskAnalyzer
from ai_project_health_monitor.core.config import get_settings
from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.evaluation.loaders import (
    load_risk_evaluation_cases,
)
from ai_project_health_monitor.evaluation.risk import RiskEvaluator
from ai_project_health_monitor.ingestion.connectors.synthetic_document import (
    SyntheticDocumentConnector,
)
from ai_project_health_monitor.ingestion.connectors.synthetic_email import (
    SyntheticEmailConnector,
)
from ai_project_health_monitor.ingestion.connectors.synthetic_jira import (
    SyntheticJiraConnector,
)
from ai_project_health_monitor.ingestion.service import IngestionService

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def build_ingestion_service() -> IngestionService:
    """Build the synthetic project ingestion service."""
    data_dir = PROJECT_ROOT / "data" / "synthetic"

    return IngestionService(
        connectors=[
            SyntheticJiraConnector(
                data_dir / "jira" / "events.json",
            ),
            SyntheticEmailConnector(
                data_dir / "emails" / "events.json",
            ),
            SyntheticDocumentConnector(
                data_dir / "documents",
            ),
        ],
    )


def build_evidence_by_event_id(
    project_id: str,
) -> dict[str, Evidence]:
    """Build an evidence lookup from synthetic project events."""
    ingestion_service = build_ingestion_service()

    events = ingestion_service.ingest_project(project_id)

    return {
        event.event_id: Evidence(
            event_id=event.event_id,
            source_type=event.source_type,
            source_id=event.source_id,
            content=event.content,
            occurred_at=event.occurred_at,
        )
        for event in events
    }


def main() -> None:
    """Run risk-analysis evaluation against the golden dataset."""
    dataset_path = (
        PROJECT_ROOT
        / "data"
        / "evaluation"
        / "risk_golden.json"
    )

    cases = load_risk_evaluation_cases(dataset_path)

    evidence_by_project: dict[str, dict[str, Evidence]] = {}
    evidence_by_case: dict[str, list[Evidence]] = {}

    for case in cases:
        if case.project_id not in evidence_by_project:
            evidence_by_project[case.project_id] = (
                build_evidence_by_event_id(case.project_id)
            )

        project_evidence = evidence_by_project[case.project_id]

        missing_event_ids = [
            event_id
            for event_id in case.evidence_event_ids
            if event_id not in project_evidence
        ]

        if missing_event_ids:
            raise ValueError(
                f"Case {case.case_id} references missing events: "
                f"{missing_event_ids}"
            )

        evidence_by_case[case.case_id] = [
            project_evidence[event_id]
            for event_id in case.evidence_event_ids
        ]

    settings = get_settings()

    llm_client = LLMClientFactory.create(settings)

    risk_analyzer = LLMRiskAnalyzer(
        llm_client=llm_client,
    )

    evaluator = RiskEvaluator(
        analyze=risk_analyzer.analyze,
    )

    evaluation_run = evaluator.evaluate(
        cases=cases,
        evidence_by_case=evidence_by_case,
    )

    summary = evaluation_run.summary

    print("=" * 80)
    print("RISK ANALYSIS EVALUATION")
    print("=" * 80)
    print(f"LLM provider      : {settings.llm_provider.value}")
    print(f"LLM model         : {settings.llm_model}")
    print()

    print(f"Total cases       : {summary.total_cases}")
    print(f"True positives    : {summary.true_positive_count}")
    print(f"False positives   : {summary.false_positive_count}")
    print(f"False negatives   : {summary.false_negative_count}")
    print(f"Precision         : {summary.precision:.4f}")
    print(f"Recall            : {summary.recall:.4f}")
    print(f"F1                : {summary.f1:.4f}")
    print(f"Severity accuracy : {summary.severity_accuracy:.4f}")
    print(f"Evidence accuracy : {summary.evidence_accuracy:.4f}")

    print("\nCASE RESULTS")
    print("=" * 80)

    for case, result in zip(
        cases,
        evaluation_run.results,
        strict=True,
    ):
        print(f"\nCase: {case.case_id}")
        print(
            f"Expected: "
            f"{[risk.value for risk in case.expected_risk_types]}"
        )
        print(
            f"Predicted: "
            f"{[risk.value for risk in result.predicted_risk_types]}"
        )
        print(
            f"TP={result.true_positive_count} "
            f"FP={result.false_positive_count} "
            f"FN={result.false_negative_count}"
        )
        print(
            f"Severity correct: {result.severity_correct}"
        )
        print(
            f"Evidence correct: {result.evidence_correct}"
        )
        print(
            f"Expected evidence: {result.expected_evidence_event_ids}"
        )
        print(
            f"Predicted evidence: {result.predicted_evidence_event_ids}"
        )


if __name__ == "__main__":
    main()