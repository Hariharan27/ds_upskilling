from abc import ABC, abstractmethod
from ast import List

from app.domain.entities.document import Document


class DocumentRepository(ABC):
    """
    Contract for document storage
    and retrieval.
    """

    @abstractmethod
    def save(self, document: Document) -> None:
        """
        Save a document.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
            self,
            document_id: str
    ) -> Document | None:
        """
        Retrieve document by ID.
        """
        raise NotImplementedError


    @abstractmethod
    def get_all(self) -> List[Document]:
        """
        Retrieve all documents.
        """

        raise NotImplementedError


