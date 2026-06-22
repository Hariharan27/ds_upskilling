from pathlib import Path

from app.application.services.metadata_resolver import (
    MetadataResolver,
)


def main() -> None:

    resolver = MetadataResolver()

    pdf_directory = Path(
        "/Users/ideas2it/Documents/Data Science &Gen AI/GenAIDataSciencePractice/iBuddy/data/incoming"
    )

    success_count = 0

    for pdf_file in sorted(
        pdf_directory.glob("*.pdf")
    ):

        try:

            metadata = resolver.resolve(
                str(pdf_file)
            )

            print(
                f"{pdf_file.name}"
                f" -> "
                f"{metadata.department.value}"
                f" | "
                f"{metadata.category.value}"
            )

            success_count += 1

        except Exception as ex:

            print(
                f"FAILED: "
                f"{pdf_file.name}"
            )

            print(ex)

    print(
        f"\nSuccessfully classified: "
        f"{success_count}"
    )


if __name__ == "__main__":
    main()