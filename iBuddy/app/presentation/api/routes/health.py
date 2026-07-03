from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def health_check() -> dict:
    """
    Health check endpoint.
    """
    return {
        "application": "iBuddy",
        "status": "running"
    }