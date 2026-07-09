from app.domain.services.date_provider import (
    DateProvider,
)
from app.infrastructure.rest.models.leave_details_request import (
    LeaveDetailsRequest,
)


class LeaveDetailsRequestMapper:

    def __init__(
            self,
            date_provider: DateProvider,
    ) -> None:
        self._date_provider = date_provider

    def map(
            self,
    ) -> LeaveDetailsRequest:
        """
        Maps the request required by the
        Leave Details REST API.
        """

        return LeaveDetailsRequest(
            year=self._date_provider.current_year(),
            quarter=self._date_provider.current_quarter(),
        )
