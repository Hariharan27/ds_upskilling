import httpx

from app.domain.services.hrms_rest_client import (
    HRMSRestClient,
)
from app.shared.config import (
    get_settings,
)
from app.domain.enums.http_method import (
    HttpMethod,
)


class HRMSRestClientImpl(HRMSRestClient):

    def __init__(
        self,
    ) -> None:
        self._settings = get_settings()
        self._client = httpx.Client(
            base_url=self._settings.HRMS_base_url,
            timeout=30,
        )

    def execute(
        self,
        endpoint: str,
        method : HttpMethod,
        query_params: dict | None = None,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> dict:

        request_headers = {
            "Authorization": (
                f"Bearer {self._settings.HRMS_auth_token}"
            ),
            "Content-Type": "application/json",
        }

        if headers:
            request_headers.update(
                headers,
            )

        response = self._client.request(
            method=method,
            url=endpoint,
            params=query_params,
            json=payload,
            headers=request_headers,
        )

        response.raise_for_status()

        return response.json()