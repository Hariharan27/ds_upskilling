import random

from app.services.prompts.versions import (
    PromptVersion
)


class PromptSelector:

    @staticmethod
    def select() -> PromptVersion:

        return random.choice(
            [
                PromptVersion.V1,
                PromptVersion.V2
            ]
        )