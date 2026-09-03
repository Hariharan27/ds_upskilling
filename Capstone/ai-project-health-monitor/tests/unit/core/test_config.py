from ai_project_health_monitor.core.config import (
    Environment,
    Settings,
    get_settings,
)


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.app_name == "AI Project Health Monitor"
    assert settings.app_version == "0.1.0"
    assert settings.environment == Environment.DEVELOPMENT
    assert settings.debug is False


def test_settings_accept_environment_values() -> None:
    settings = Settings(environment="testing")

    assert settings.environment == Environment.TESTING


def test_settings_reject_invalid_environment() -> None:
    invalid_settings = {"environment": "invalid"}

    try:
        Settings(**invalid_settings)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid environment should raise ValueError")


def test_get_settings_returns_cached_instance() -> None:
    get_settings.cache_clear()

    first = get_settings()
    second = get_settings()

    assert first is second