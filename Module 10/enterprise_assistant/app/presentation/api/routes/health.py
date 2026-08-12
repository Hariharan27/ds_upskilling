from fastapi import APIRouter, Depends

from app.presentation.api.schemas.health import HealthResponse
from app.shared.config import Settings, get_settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(
    settings: Settings = Depends(get_settings),
) -> HealthResponse:
    """Return the current application health status."""

    return HealthResponse(
        status="ok",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )