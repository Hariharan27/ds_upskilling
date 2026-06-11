from app.services.prompts.classifier_prompt import (
    SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES,
    OUTPUT_SCHEMA
)

def build_classification_prompt(
    employee_message: str
) -> str:

    return f"""
{SYSTEM_PROMPT}

{FEW_SHOT_EXAMPLES}

{OUTPUT_SCHEMA}

Employee Request:

{employee_message}
"""