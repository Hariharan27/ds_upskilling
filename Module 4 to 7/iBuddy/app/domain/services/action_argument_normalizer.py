from abc import ABC
from abc import abstractmethod

from pydantic import BaseModel


class ActionArgumentNormalizer(
    ABC,
):
    """
    Normalizes action arguments before validation.
    """

    @abstractmethod
    def normalize(
        self,
        arguments: BaseModel,
    ) -> BaseModel:
        """
        Normalize extracted action arguments.
        """
        ...