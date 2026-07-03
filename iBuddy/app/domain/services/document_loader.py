from abc import ABC, abstractmethod

from app.domain.entities.document import Document
from app.domain.value_objects.document_metadata import DocumentMetadata


class DocumentLoader(ABC):
    """
    Contract for loading documents
    from a source file.
    """

    @abstractmethod
    def load(
        self,
        file_path: str,
        metadata: DocumentMetadata,
    ) -> Document:
        """
        Load a file and convert it
        into a Document entity.
        """
        raise NotImplementedError