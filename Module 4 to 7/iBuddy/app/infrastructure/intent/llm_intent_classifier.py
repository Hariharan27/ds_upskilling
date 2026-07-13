import json

from app.application.services.intent.intent_prompt_builder import IntentPromptBuilder
from app.domain.models.intent_classification_request import IntentClassificationRequest
from app.domain.models.intent_classification_result import IntentClassificationResult
from app.domain.services.intent_classifier import IntentClassifier
from app.domain.services.llm_client import LLMClient


class LLMIntentClassifier(IntentClassifier):

    def __init__(
            self,
            prompt_builder: IntentPromptBuilder,
            llm_client: LLMClient,):
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def classify(self,request: IntentClassificationRequest) -> IntentClassificationResult:

         llm_request = self.prompt_builder.build(request)

         llm_response  = self.llm_client.generate_text(llm_request)

         response = json.loads(
             llm_response.content,
         )

         return IntentClassificationResult(
             tool_name=response.get(
                 "tool_name",
             ),
             confidence=response["confidence"],
             reason=response["reason"],
         )



