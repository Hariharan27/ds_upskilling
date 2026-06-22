from pathlib import Path

import fitz

from app.domain.entities.document import Document
from app.domain.services.document_loader import DocumentLoader
from app.shared.exceptions.document_load_exception import (
    DocumentLoadException,
)


class PdfDocumentLoader(DocumentLoader):
    """
    Loads PDF documents using PyMuPDF.
    """

    def load(
        self,
        file_path: str,
    ) -> Document:
        """
        Load a PDF file and convert it
        into a Document entity.
        """

        path = Path(file_path)

        if not path.exists():
            raise DocumentLoadException(
                f"PDF file does not exist: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise DocumentLoadException(
                f"Unsupported file type: {path.suffix}"
            )

        try:
            content_parts: list[str] = []

            with fitz.open(file_path) as pdf_document:
                for page in pdf_document:
                    content_parts.append(page.get_text())

            content = "\n".join(content_parts).strip()

            if not content:
                raise DocumentLoadException(
                    f"PDF contains no extractable text: {file_path}"
                )

            return Document(
                document_id=path.stem,
                file_name=path.name,
                file_path=str(path),
                content=content,
                metadata={},
            )

        except DocumentLoadException:
            raise

        except Exception as ex:
            raise DocumentLoadException(
                f"Failed to load PDF: {file_path}"
            ) from ex