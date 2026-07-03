from app.core.config import settings

from app.schemas.response import (
    CostResponse,
)


class CostCalculator:
    @staticmethod
    def calculate(
        input_tokens: int,
        output_tokens: int,
    ) -> CostResponse:
        input_cost = (
            input_tokens / 1_000_000
        ) * settings.MODEL_INPUT_COST_PER_MILLION

        output_cost = (
            output_tokens / 1_000_000
        ) * settings.MODEL_OUTPUT_COST_PER_MILLION

        total_cost = input_cost + output_cost

        return CostResponse(
            input_cost_usd=round(input_cost, 8),
            output_cost_usd=round(output_cost, 8),
            total_cost_usd=round(total_cost, 8),
        )