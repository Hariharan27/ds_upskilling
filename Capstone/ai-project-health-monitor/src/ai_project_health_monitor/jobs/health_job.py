import sys

from ai_project_health_monitor.api.dependencies import get_application_container


def run(project_id: str) -> None:
    """Run the end-to-end project health monitoring job."""
    if not project_id.strip():
        raise ValueError("project_id cannot be empty")

    container = get_application_container()

    print("=" * 60)
    print("AI PROJECT HEALTH MONITOR JOB")
    print("=" * 60)
    print(f"Project: {project_id}")
    print()

    print("[1] Ingestion + indexing + health analysis...")
    result = container.project_health_monitor.run_job(project_id)

    health_state = result.health_state
    health_score = health_state.health_score

    print()
    print("[2] Ingestion")
    print(f"    Events ingested: {result.events_ingested}")

    print()
    print("[3] RAG indexing")
    print(f"    Chunks indexed: {result.chunks_indexed}")

    print()
    print("[4] Evidence state")
    print(f"    Evidence changed: {result.evidence_changed}")

    print()
    print("[5] Health")
    print(f"    Score:  {health_score.score if health_score else 'N/A'}")
    print(f"    Status: {health_score.status if health_score else 'N/A'}")
    print(f"    Risks:  {len(health_state.risk_signals)}")

    print()
    print("[6] Summary")
    if health_state.summary is not None:
        print(f"    {health_state.summary.executive_summary}")
        print()
        print("    Recommended actions:")
        for action in health_state.summary.recommended_actions:
            print(f"      - {action}")
    else:
        print("    No summary generated.")

    print()
    print("[7] Alert")
    print(f"    Triggered: {health_state.alert_triggered}")

    print()
    print("=" * 60)
    print("JOB COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: uv run python -m "
            "ai_project_health_monitor.jobs.health_job <project_id>"
        )

    run(sys.argv[1])