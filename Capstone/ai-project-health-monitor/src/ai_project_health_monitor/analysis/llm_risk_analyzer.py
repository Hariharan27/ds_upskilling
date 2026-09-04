import json
from uuid import uuid4

from pydantic import BaseModel, Field

from ai_project_health_monitor.analysis.llm import LLMClient
from ai_project_health_monitor.analysis.risk_analyzer import RiskAnalyzer
from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.domain.models.risk_signal import (
    RiskSeverity,
    RiskSignal,
    RiskType,
)


class RiskAnalysisResponse(BaseModel):
    """Structured response returned by the risk-analysis model."""

    risk_type: RiskType
    severity: RiskSeverity
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_source_id: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


class LLMRiskAnalyzer(RiskAnalyzer):
    """Extract evidence-backed risk signals using an LLM."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm_client = llm_client

    def analyze(
        self,
        project_id: str,
        evidence: list[Evidence],
    ) -> list[RiskSignal]:
        """Analyze evidence and return validated risk signals."""
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        if not evidence:
            return []

        prompt = self._build_prompt(project_id, evidence)
        response = self._llm_client.generate(prompt)

        return self._parse_response(
            project_id=project_id,
            evidence=evidence,
            response=response,
        )

    def _build_prompt(
        self,
        project_id: str,
        evidence: list[Evidence],
    ) -> str:
        evidence_text = "\n\n".join(
            (
                f"Source ID: {item.source_id}\n"
                f"Source Type: {item.source_type.value}\n"
                f"Occurred At: {item.occurred_at.isoformat()}\n"
                f"Content: {item.content}"
            )
            for item in evidence
        )

        return f"""
Analyze the following project evidence for project {project_id}.

Identify only risks that are directly supported by the evidence.

Allowed risk types:
- delay
- blocker
- scope_creep
- client_sentiment
- resource
- dependency
- delivery

Allowed severity values:
- low
- medium
- high
- critical

Each object must contain exactly these fields:
- risk_type: one of "delay", "blocker", "scope_creep",
  "client_sentiment", "resource", "dependency", "delivery"
- severity: one of "low", "medium", "high", "critical"
- confidence: a NUMBER between 0.0 and 1.0, NOT a word or label
- evidence_source_id: must exactly match one of the provided Source IDs
- rationale: a concise explanation grounded in the evidence

Example of a valid confidence value:
0.95

Invalid confidence values:
"high"
"95%"
"very confident"

If no risk is supported by the evidence, return an empty JSON array.

Return ONLY a valid JSON array.
Do not include Markdown code fences.
Do not include explanations outside the JSON array.

Evidence:

{evidence_text}
""".strip()

    def _parse_response(
        self,
        project_id: str,
        evidence: list[Evidence],
        response: str,
    ) -> list[RiskSignal]:
        try:
            raw_response = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError("LLM response must contain valid JSON") from exc

        if not isinstance(raw_response, list):
            raise ValueError("LLM response must be a JSON array")

        evidence_by_source_id = {
            item.source_id: item
            for item in evidence
        }

        signals: list[RiskSignal] = []

        for item in raw_response:
            parsed = RiskAnalysisResponse.model_validate(item)

            source_evidence = evidence_by_source_id.get(
                parsed.evidence_source_id
            )

            if source_evidence is None:
                raise ValueError(
                    "LLM referenced evidence that was not provided"
                )

            signals.append(
                RiskSignal(
                    signal_id=f"RISK-{uuid4()}",
                    project_id=project_id,
                    event_id=source_evidence.event_id,
                    risk_type=parsed.risk_type,
                    severity=parsed.severity,
                    confidence=parsed.confidence,
                    evidence=source_evidence,
                    rationale=parsed.rationale,
                )
            )

        return signals