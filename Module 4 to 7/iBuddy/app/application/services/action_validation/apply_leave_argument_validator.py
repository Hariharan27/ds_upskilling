from datetime import datetime

from app.application.services.action_argument_extraction.models import (
    ApplyLeaveArguments,
)
from app.application.services.action_validation.action_argument_validator import (
    ActionArgumentValidator,
)
from app.application.services.action_validation.models import (
    ActionValidationResult,
    ValidationError,
)


class ApplyLeaveArgumentValidator(
    ActionArgumentValidator,
):
    """
    Validates normalized Apply Leave arguments before tool execution.
    """

    ALLOWED_LEAVE_TYPES = {
        "Work From Home",
        "Casual Leave",
        "Sick Leave",
        "Privilege Leave",
    }

    def validate(
        self,
        arguments: ApplyLeaveArguments,
    ) -> ActionValidationResult:

        result = super().validate(
            arguments,
        )

        missing_fields = list(
            result.missing_fields,
        )

        invalid_fields = list(
            result.invalid_fields,
        )

        #
        # Duration is only an intermediate field used by the
        # normalizer to derive leave_end_date.
        #
        if "leave_duration" in missing_fields:
            missing_fields.remove(
                "leave_duration",
            )

        #
        # Backend requires leave_end_date.
        #
        if (
            not arguments.leave_end_date
            and "leave_end_date"
            not in missing_fields
        ):
            missing_fields.append(
                "leave_end_date",
            )

        self._validate_leave_type(
            arguments.leave_type,
            invalid_fields,
        )

        self._validate_date(
            field_name="leave_start_date",
            value=arguments.leave_start_date,
            invalid_fields=invalid_fields,
        )

        self._validate_date(
            field_name="leave_end_date",
            value=arguments.leave_end_date,
            invalid_fields=invalid_fields,
        )

        self._validate_date_range(
            arguments,
            invalid_fields,
        )

        return ActionValidationResult(
            is_valid=(
                not missing_fields
                and not invalid_fields
            ),
            missing_fields=missing_fields,
            invalid_fields=invalid_fields,
        )

    def _validate_leave_type(
        self,
        leave_type: str | None,
        invalid_fields: list[ValidationError],
    ) -> None:

        if leave_type is None:
            return

        if leave_type not in self.ALLOWED_LEAVE_TYPES:

            invalid_fields.append(
                ValidationError(
                    field="leave_type",
                    code="INVALID_LEAVE_TYPE",
                )
            )

    def _validate_date(
        self,
        field_name: str,
        value: str | None,
        invalid_fields: list[ValidationError],
    ) -> None:

        if value is None:
            return

        if not self._is_valid_iso_date(
            value,
        ):
            invalid_fields.append(
                ValidationError(
                    field=field_name,
                    code="INVALID_DATE_FORMAT",
                )
            )

    def _validate_date_range(
        self,
        arguments: ApplyLeaveArguments,
        invalid_fields: list[ValidationError],
    ) -> None:

        if (
            not arguments.leave_start_date
            or not arguments.leave_end_date
        ):
            return

        if (
            not self._is_valid_iso_date(
                arguments.leave_start_date,
            )
            or not self._is_valid_iso_date(
                arguments.leave_end_date,
            )
        ):
            return

        start_date = datetime.strptime(
            arguments.leave_start_date,
            "%Y-%m-%d",
        ).date()

        end_date = datetime.strptime(
            arguments.leave_end_date,
            "%Y-%m-%d",
        ).date()

        if start_date > end_date:

            invalid_fields.append(
                ValidationError(
                    field="leave_end_date",
                    code="INVALID_DATE_RANGE",
                )
            )

    @staticmethod
    def _is_valid_iso_date(
        value: str,
    ) -> bool:
        """
        Validates ISO-8601 date format (YYYY-MM-DD).
        """

        try:

            datetime.strptime(
                value,
                "%Y-%m-%d",
            )

            return True

        except ValueError:

            return False