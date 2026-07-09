from abc import ABC, abstractmethod

from app.domain.models.intent_classification_request import IntentClassificationRequest
from app.domain.models.intent_classification_result import IntentClassificationResult

class IntentClassifier(ABC):

    """
    Contract for determining how a user request should be processed.

    Implementations may use an LLM, rules, or any other strategy to classify
    the user's intent.
    """
    @abstractmethod
    def classify(self,request: IntentClassificationRequest) -> IntentClassificationResult:
        """
        Classify the user's request and determine the execution pipeline.
        """
        pass