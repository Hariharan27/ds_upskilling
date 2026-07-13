from app.application.services.action_argument_extraction.models import (
    ApplyLeaveArguments,
)
from app.application.services.action_argument_extraction.relative_date_resolver import (
    RelativeDateResolver,
)
from app.domain.services.action_argument_normalizer import (
    ActionArgumentNormalizer,
)


class ApplyLeaveArgumentNormalizer(
    ActionArgumentNormalizer,
):
    """
    Normalizes Apply Leave arguments.
    """

    def __init__(
        self,
        relative_date_resolver: RelativeDateResolver,
    ) -> None:
        self._relative_date_resolver = (
            relative_date_resolver
        )

    def normalize(
        self,
        arguments: ApplyLeaveArguments,
    ) -> ApplyLeaveArguments:

        arguments.leave_start_date = (
            self._relative_date_resolver.resolve(
                arguments.leave_start_date,
            )
        )

        arguments.leave_end_date = (
            self._relative_date_resolver.resolve(
                arguments.leave_end_date,
            )
        )

        arguments.leave_end_date = (
            self._relative_date_resolver.resolve_end_date(
                start_date=arguments.leave_start_date,
                end_date=arguments.leave_end_date,
                duration=arguments.leave_duration,
            )
        )

        return arguments