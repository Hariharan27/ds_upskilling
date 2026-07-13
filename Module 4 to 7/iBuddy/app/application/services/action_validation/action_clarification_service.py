from app.application.services.action_validation.models import (
    ActionValidationResult,
)


class ActionClarificationService:
    """
    Builds a clarification message for missing action arguments.
    """

    def __init__(
        self,
        field_labels: dict[str, str],
    ) -> None:
        self._field_labels = field_labels

    def build(
        self,
        validation_result: ActionValidationResult,
    ) -> str:
        if validation_result.is_valid:
            return ""

        missing_fields = [
            self._field_labels.get(
                field,
                field.replace("_", " "),
            )
            for field in validation_result.missing_fields
        ]

        fields = "\n".join(
            f"• {field}"
            for field in missing_fields
        )

        return (
            "Before I can complete your request, "
            "I need the following information:\n\n"
            f"{fields}"
        )