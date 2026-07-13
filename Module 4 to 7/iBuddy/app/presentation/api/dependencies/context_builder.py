from app.domain.services.context_builder import (
    ContextBuilder,
)
from app.application.services.context_builder.default_context_builder import (
    DefaultContextBuilder,
)

def get_context_builder() -> ContextBuilder:

    return DefaultContextBuilder()