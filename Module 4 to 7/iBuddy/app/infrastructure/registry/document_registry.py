import json

from pathlib import Path

from dataclasses import asdict

from app.application.dto.document_registry_entry import (
    DocumentRegistryEntry,
)

class JsonDocumentRegistry:
    """
    JSON-backed document registry.
    """

    def __init__(
        self,
        registry_path: str = (
            "data/document_registry.json"
        ),
    ) -> None:

        self._registry_path = Path(
            registry_path
        )

        self._ensure_registry_exists()

    def _ensure_registry_exists(
        self,
    ) -> None:

        if not self._registry_path.exists():

            self._registry_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._registry_path.write_text(
                "{}"
            )

    def load(
            self,
    ) -> dict:
        with open(
                self._registry_path,
                "r",
                encoding="utf-8",
        ) as file:
            return json.load(file)

    def save(
            self,
            data: dict,
    ) -> None:
        with open(
                self._registry_path,
                "w",
                encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

    def get_document(
            self,
            file_name: str,
    ) -> dict | None:
        registry = self.load()

        return registry.get(file_name)

    def upsert_document(
            self,
            entry: DocumentRegistryEntry,
    ) -> None:
        registry = self.load()

        registry[entry.file_name] = asdict(
            entry
        )

        self.save(registry)

    def is_document_changed(
            self,
            file_name: str,
            current_hash: str,
    ) -> bool:
        """
        Returns True when a document
        should be indexed.
        """

        document = self.get_document(
            file_name
        )

        if document is None:
            return True

        return (
                document["file_hash"]
                != current_hash
        )


