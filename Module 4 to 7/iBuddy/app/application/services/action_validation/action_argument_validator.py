from pydantic import BaseModel

from app.application.services.action_validation.models import (
    ActionValidationResult,
)


class ActionArgumentValidator:
    """
    Validates extracted arguments for ACTION tools.
    """

    def validate(
        self,
        arguments: BaseModel,
    ) -> ActionValidationResult:

        missing_fields = [
            field_name
            for field_name, value in arguments.model_dump().items()
            if self._is_missing(
                value,
            )
        ]

        return ActionValidationResult(
            is_valid=not missing_fields,
            missing_fields=missing_fields,
        )

    @staticmethod
    def _is_missing(
        value: object,
    ) -> bool:
        """
        Determines whether a value should be considered missing.
        """

        if value is None:
            return True

        if isinstance(
            value,
            str,
        ):
            return value.strip() == ""

        return False