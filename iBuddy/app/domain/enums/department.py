from enum import Enum


class Department(str, Enum):
    """
    Supported document departments.
    """

    HR = "HR"

    CORPORATE_GOVERNANCE = (
        "CORPORATE_GOVERNANCE"
    )

    IT_SECURITY = "IT_SECURITY"