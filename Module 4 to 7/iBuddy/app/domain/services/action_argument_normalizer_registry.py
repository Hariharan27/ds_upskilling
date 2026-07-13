from app.domain.services.action_argument_normalizer import (
    ActionArgumentNormalizer,
)


class ActionArgumentNormalizerRegistry:

    def __init__(self) -> None:
        self._normalizers: dict[
            str,
            ActionArgumentNormalizer,
        ] = {}

    def register(
        self,
        tool_name: str,
        normalizer: ActionArgumentNormalizer,
    ) -> None:

        self._normalizers[
            tool_name
        ] = normalizer

    def get(
        self,
        tool_name: str,
    ) -> ActionArgumentNormalizer:

        return self._normalizers[
            tool_name
        ]