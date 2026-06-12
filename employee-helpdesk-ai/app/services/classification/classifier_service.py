import json

from app.services.llm.together_client import (
    TogetherClient
)

from app.services.prompts.prompt_builder import (
    build_messages
)
from app.schemas.response import (
    TicketClassificationResponse
)



class ClassifierService:

    def __init__(self):
        self.llm_client = TogetherClient()

    def classify(
            self,
            employee_message: str
    ):
        messages = build_messages(employee_message)

        response = self.llm_client.generate(
            messages=messages
        )

        response_data = json.loads(
            response.content
        )

        classification = (
            TicketClassificationResponse(
                **response_data
            )
        )

        return classification