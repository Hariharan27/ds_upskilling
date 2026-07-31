from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response returned by the application health endpoint."""

    status: str
    application: str
    version: str
    environment: str