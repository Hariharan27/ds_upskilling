from enum import Enum


class ExecutionType(str, Enum):
    QUERY = "QUERY"
    ACTION = "ACTION"