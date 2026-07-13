from pathlib import Path

from app.application.services.metadata_mappings import (
    DOCUMENT_METADATA_MAPPING,
)

from app.domain.value_objects.document_metadata import (
    DocumentMetadata,
)


class MetadataResolver:

    def resolve(
        self,
        file_path: str,
    ) -> DocumentMetadata:

        file_name = (
            Path(file_path)
            .name
            .lower()
        )

        for (
            keyword,
            metadata,
        ) in DOCUMENT_METADATA_MAPPING.items():

            if keyword in file_name:

                department, category = metadata

                return DocumentMetadata(
                    department=department,
                    category=category,
                )

        raise ValueError(
            f"Unsupported document: {file_name}"
        )