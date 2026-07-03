from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    summary="Health",
    description="Health check",
    )
async def health_check() -> dict[str, str]:
    return { "status": "healthy" }