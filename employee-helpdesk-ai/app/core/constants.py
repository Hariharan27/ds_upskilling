from typing import Literal


SUPPORTED_DEPARTMENTS = [
    "HR",
    "IT_SUPPORT",
    "ADMIN_FACILITIES"
]

PROMPT_INJECTION_THRESHOLD = 3

MAX_MESSAGE_LENGTH = 2000


SYSTEM_ROLE: Literal["system"] = "system"
USER_ROLE: Literal["user"] = "user"