import pytest

from ai_project_health_monitor.ingestion.connectors.base import (
    ProjectSourceConnector,
)
from ai_project_health_monitor.ingestion.normalizer import EventNormalizer


def test_project_source_connector_is_abstract() -> None:
    with pytest.raises(TypeError):
        ProjectSourceConnector()


def test_event_normalizer_is_abstract() -> None:
    with pytest.raises(TypeError):
        EventNormalizer()