from datetime import date

import pytest
from pydantic import ValidationError

from ai_project_health_monitor.domain.models.project import (
    Project,
    ProjectStatus,
)


def test_project_defaults_to_active() -> None:
    project = Project(
        project_id="PROJ-001",
        name="Customer Portal",
    )

    assert project.status == ProjectStatus.ACTIVE

def test_project_accepts_valid_dates() -> None:
    project = Project(
        project_id="PROJ-001",
        name="Customer Portal",
        start_date=date(2026, 1, 1),
        target_end_date=date(2026, 6, 30),
    )

    assert project.start_date == date(2026, 1, 1)
    assert project.target_end_date == date(2026, 6, 30)


@pytest.mark.parametrize(
    "field",
    ["project_id", "name"],
)
def test_project_rejects_empty_required_fields(field: str) -> None:
    data = {
        "project_id": "PROJ-001",
        "name": "Customer Portal",
    }
    data[field] = ""

    with pytest.raises(ValidationError):
        Project(**data)


def test_project_status_is_validated() -> None:
    project = Project(
        project_id="PROJ-001",
        name="Customer Portal",
        status="on_hold",
    )

    assert project.status == ProjectStatus.ON_HOLD
