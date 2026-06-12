from together.types.chat.completion_create_params import MessageChatCompletionSystemMessageParam, \
    MessageChatCompletionUserMessageParam

from app.services.prompts.classifier_prompt import (
    SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
    OUTPUT_SCHEMA
)

from together.types.chat import completion_create_params

from app.core.constants import (
    USER_ROLE,
    SYSTEM_ROLE
)

def build_messages(
    employee_message: str
) -> list[completion_create_params.Message]:

    user_prompt = f"""
{FEW_SHOT_EXAMPLES}

{OUTPUT_SCHEMA}

Employee Request:

{employee_message}
"""

    messages: list[completion_create_params.Message] = [
        MessageChatCompletionSystemMessageParam(
            content=SYSTEM_PROMPT,
            role=SYSTEM_ROLE
        ),
        MessageChatCompletionUserMessageParam(
            content=user_prompt,
            role= USER_ROLE
        )

    ]

    return messages