from datetime import date

from app.domain.services.date_provider import (
    DateProvider,
)


class SystemDateProvider(DateProvider):

    def current_date(
        self,
    ) -> date:

        return date.today()

    def current_year(self) -> int:
        return date.today().year

    def current_quarter(self) -> int:

        month = date.today().month

        return ((month - 1) // 3) + 1