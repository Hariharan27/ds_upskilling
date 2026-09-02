from typing import Literal

from pydantic import BaseModel, Field


class RouteDecision(BaseModel):
    intent: Literal[
        "policy",
        "attendance",
        "leave",
        "wfh",
        "ticket",
        "unknown",
    ] = Field(
        description="The capability that should handle the employee request."
    )