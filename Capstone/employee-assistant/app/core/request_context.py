from contextvars import ContextVar
from uuid import uuid4


request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="",
)


def create_request_id() -> str:
    return str(uuid4())


def get_request_id() -> str:
    return request_id_context.get()