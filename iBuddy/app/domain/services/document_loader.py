from abc import ABC, abstractmethod

from app.domain.entities.document import Document


class DocumentLoader(ABC):
    """
    Contract for loading documents
    from a source file.
    """

    @abstractmethod
    def load(
        self,
        file_path: str
    ) -> Document:
        """
        Load a file and convert it
        into a Document entity.
        """
        raise NotImplementedError