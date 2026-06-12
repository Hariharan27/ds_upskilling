from together.types.chat.completion_create_params import MessageChatCompletionSystemMessageParam, \
    MessageChatCompletionUserMessageParam

from app.services.prompts.classifier_prompt_v1 import (
    SYSTEM_PROMPT as SYSTEM_PROMPT_V1,
    FEW_SHOT_EXAMPLES as FEW_SHOT_EXAMPLES_V1,
    OUTPUT_SCHEMA as OUTPUT_SCHEMA_V1
)

from app.services.prompts.classifier_prompt_v2 import (
    SYSTEM_PROMPT as SYSTEM_PROMPT_V2,
    FEW_SHOT_EXAMPLES as FEW_SHOT_EXAMPLES_V2,
    OUTPUT_SCHEMA as OUTPUT_SCHEMA_V2
)

from together.types.chat import completion_create_params

from app.core.constants import (
    USER_ROLE,
    SYSTEM_ROLE
)
from app.services.prompts.versions import PromptVersion


def build_messages(
    employee_message: str,
    version: PromptVersion
) -> list[completion_create_params.Message]:

    if version == PromptVersion.V1:

        system_prompt = SYSTEM_PROMPT_V1

        few_shot_examples = FEW_SHOT_EXAMPLES_V1

        output_schema = OUTPUT_SCHEMA_V1

    elif version == PromptVersion.V2:

        system_prompt = SYSTEM_PROMPT_V2

        few_shot_examples = FEW_SHOT_EXAMPLES_V2

        output_schema = OUTPUT_SCHEMA_V2

    else:

        raise ValueError(
            f"Unsupported prompt version: {version}"
        )

    user_prompt = f"""
    {few_shot_examples}

    {output_schema}

    Employee Request:

    {employee_message}
    """

    messages: list[completion_create_params.Message] = [
            MessageChatCompletionSystemMessageParam(
                content=system_prompt,
                role=SYSTEM_ROLE
            ),
            MessageChatCompletionUserMessageParam(
                content=user_prompt,
                role= USER_ROLE
            )

        ]

    return messages