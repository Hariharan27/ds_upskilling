from datetime import (
    date,
    datetime,
    timedelta,
)
import re


class RelativeDateResolver:
    """
    Resolves natural language date expressions into ISO-8601 dates.

    Also derives an end date when a start date and duration
    are available.

    Business validation is intentionally outside this class.
    """

    def resolve(
        self,
        value: str | None,
    ) -> str | None:

        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        result = self._resolve_relative_date(
            value,
        )

        if result is not None:
            return result

        result = self._resolve_weekday(
            value,
        )

        if result is not None:
            return result

        result = self._resolve_absolute_date(
            value,
        )

        if result is not None:
            return result

        return value

    def resolve_end_date(
            self,
            start_date: str | None,
            end_date: str | None,
            duration: str | None,
    ) -> str | None:
        """
        Derives the leave end date.

        Rules

        - Existing end date always wins.
        - Start date is required.
        - If neither end date nor duration is provided,
          assume a single-day leave.
        - If duration is provided, derive the end date.
        - Unknown duration leaves the value unchanged.
        """

        #
        # Existing end date always wins.
        #
        if end_date:
            return end_date

        #
        # Cannot derive without a start date.
        #
        if not start_date:
            return None

        #
        # Single-day leave.
        #
        if not duration:
            return start_date

        duration_days = self._parse_duration(
            duration,
        )

        if duration_days is None:
            return None

        try:

            start = datetime.strptime(
                start_date,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            return None

        return (
                start +
                timedelta(
                    days=duration_days - 1,
                )
        ).isoformat()

    def _parse_duration(
        self,
        value: str,
    ) -> int | None:
        """
        Supports

        1 day
        2 days
        3 days
        ...
        """

        match = re.fullmatch(
            r"(\d+)\s+day[s]?",
            value.strip().lower(),
        )

        if not match:
            return None

        return int(
            match.group(1),
        )

    def _resolve_relative_date(
        self,
        value: str,
    ) -> str | None:

        normalized = value.lower()

        today = date.today()

        mapping = {
            "today": 0,
            "tomorrow": 1,
            "yesterday": -1,
            "day after tomorrow": 2,
        }

        offset = mapping.get(
            normalized,
        )

        if offset is None:
            return None

        return (
            today +
            timedelta(days=offset)
        ).isoformat()

    def _resolve_weekday(
        self,
        value: str,
    ) -> str | None:
        return None

    def _resolve_absolute_date(
        self,
        value: str,
    ) -> str | None:

        supported_formats = (
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d %b %Y",
            "%d %B %Y",
            "%d %b",
            "%d %B",
            "%b %d",
            "%B %d",
        )

        for date_format in supported_formats:

            try:

                parsed_date = datetime.strptime(
                    value,
                    date_format,
                )

                if "%Y" not in date_format:

                    parsed_date = parsed_date.replace(
                        year=date.today().year,
                    )

                return (
                    parsed_date.date()
                    .isoformat()
                )

            except ValueError:
                continue

        return None