from abc import ABC, abstractmethod
from app.domain.enums.http_method import (
    HttpMethod,
)

class HRMSRestClient(ABC):

    @abstractmethod
    def execute (
            self,
            endpoint: str,
            method: HttpMethod,
            query_params: dict | None = None,
            payload: dict|None = None,
            headers: dict|None = None,
    ) -> dict:
        """
        Execute an HRMS REST API request.
        """
        pass
