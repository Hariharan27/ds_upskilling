from abc import ABC
from abc import abstractmethod
from datetime import date


class DateProvider(ABC):

    @abstractmethod
    def current_date(
        self,
    ) -> date:
        """
        Returns the current system date.
        """
        pass

    @abstractmethod
    def current_year(self) -> int:
        pass

    @abstractmethod
    def current_quarter(self) -> int:
        pass