import os
from pathlib import Path
from typing import Any

import chromadb
import fitz
from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import Field
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

COLLECTION_NAME = "company_documents"

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

LLM_MODEL_NAME = (
        "together_ai/"
        "meta-llama/"
        "Llama-3.3-70B-Instruct-Turbo"
)

# ---------------------------------------------------------
# PDF Loading
# ---------------------------------------------------------


def load_pdf_pages(
    pdf_path: Path,
) -> list[dict[str, Any]]:
    """
    Extract text from a PDF page by page.

    Each returned item contains:
    - text
    - source
    - page_number
    """

    pages = []

    with fitz.open(pdf_path) as document:
        for page_index, page in enumerate(document):
            text = page.get_text().strip()

            if not text:
                continue

            pages.append(
                {
                    "text": text,
                    "source": pdf_path.name,
                    "page_number": page_index + 1,
                }
            )

    return pages


def load_all_pdf_pages() -> list[dict[str, Any]]:
    """
    Load all PDF files from the data directory.
    """

    pages = []

    pdf_files = list(
        DATA_DIR.glob("*.pdf")
    )

    if not pdf_files:
        raise ValueError(
            f"No PDF files found in {DATA_DIR}"
        )

    for pdf_path in pdf_files:
        print(
            f"[LOADING PDF] {pdf_path.name}"
        )

        pdf_pages = load_pdf_pages(
            pdf_path
        )

        pages.extend(
            pdf_pages
        )

    return pages


# ---------------------------------------------------------
# Text Chunking
# ---------------------------------------------------------


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """
    Split text into overlapping character-based chunks.

    This is intentionally simple for the CrewAI playground.
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[
            start:end
        ].strip()

        if chunk:
            chunks.append(
                chunk
            )

        if end >= len(text):
            break

        start += (
            chunk_size
            - chunk_overlap
        )

    return chunks


def create_document_chunks(
    pages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Convert PDF pages into smaller searchable chunks.
    """

    document_chunks = []

    for page in pages:
        chunks = chunk_text(
            page["text"]
        )

        for chunk_index, chunk in enumerate(chunks):
            document_chunks.append(
                {
                    "text": chunk,
                    "source": page["source"],
                    "page_number": page[
                        "page_number"
                    ],
                    "chunk_index": chunk_index,
                }
            )

    return document_chunks


# ---------------------------------------------------------
# ChromaDB Indexing
# ---------------------------------------------------------


def create_document_collection(
    embedding_model: SentenceTransformer,
):
    """
    Load PDFs, create chunks, generate embeddings,
    and store everything in ChromaDB.
    """

    client = chromadb.Client()

    collection = (
        client.get_or_create_collection(
            name=COLLECTION_NAME
        )
    )

    pages = load_all_pdf_pages()

    document_chunks = (
        create_document_chunks(
            pages
        )
    )

    if not document_chunks:
        raise ValueError(
            "No readable text was found "
            "inside the PDF documents."
        )

    texts = [
        chunk["text"]
        for chunk in document_chunks
    ]

    print(
        f"\n[INDEXING] "
        f"{len(texts)} chunks"
    )

    embeddings = (
        embedding_model.encode(
            texts,
            normalize_embeddings=True,
        ).tolist()
    )

    ids = []

    metadatas = []

    for index, chunk in enumerate(
        document_chunks
    ):
        chunk_id = (
            f"{chunk['source']}"
            f"-page-{chunk['page_number']}"
            f"-chunk-{chunk['chunk_index']}"
            f"-{index}"
        )

        ids.append(
            chunk_id
        )

        metadatas.append(
            {
                "source": chunk[
                    "source"
                ],
                "page_number": chunk[
                    "page_number"
                ],
                "chunk_index": chunk[
                    "chunk_index"
                ],
            }
        )

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        "[INDEXING COMPLETED]"
    )

    return collection


# ---------------------------------------------------------
# CrewAI Document Search Tool
# ---------------------------------------------------------


class DocumentSearchTool(BaseTool):
    name: str = (
        "company_document_search"
    )

    description: str = (
        "Search the company's internal PDF policy "
        "documents for information relevant to an "
        "employee's question. "
        "Always use this tool before answering questions "
        "about company policies, leave, WFH, benefits, "
        "or other internal company information."
    )

    collection: Any = Field(
        exclude=True
    )

    embedding_model: Any = Field(
        exclude=True
    )

    def _run(
        self,
        query: str,
    ) -> str:
        """
        Retrieve relevant chunks from ChromaDB.
        """

        print(
            f"\n[DOCUMENT SEARCH]"
            f"\nQuery: {query}"
        )

        query_embedding = (
            self.embedding_model.encode(
                query,
                normalize_embeddings=True,
            ).tolist()
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=5,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = (
            results.get(
                "documents",
                [[]],
            )[0]
        )

        metadatas = (
            results.get(
                "metadatas",
                [[]],
            )[0]
        )

        distances = (
            results.get(
                "distances",
                [[]],
            )[0]
        )

        if not documents:
            return (
                "No relevant information was found "
                "in the company documents."
            )

        retrieved_context = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            source = metadata.get(
                "source",
                "Unknown",
            )

            page_number = metadata.get(
                "page_number",
                "Unknown",
            )

            retrieved_context.append(
                (
                    f"Source: {source}\n"
                    f"Page: {page_number}\n"
                    f"Distance: {distance}\n"
                    f"Content:\n{document}"
                )
            )

        return "\n\n---\n\n".join(
            retrieved_context
        )


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------


def load_api_key() -> str:
    """
    Load Together AI API key.
    """

    env_path = BASE_DIR / ".env"

    load_dotenv(
        dotenv_path=env_path
    )

    api_key = os.getenv(
        "TOGETHER_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "TOGETHER_API_KEY is not configured."
        )

    return api_key


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------


def main() -> None:
    api_key = load_api_key()

    # -----------------------------------------------------
    # Embedding Model
    # -----------------------------------------------------

    embedding_model = (
        SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )
    )

    # -----------------------------------------------------
    # Build PDF Index
    # -----------------------------------------------------

    collection = (
        create_document_collection(
            embedding_model
        )
    )

    # -----------------------------------------------------
    # Create CrewAI Search Tool
    # -----------------------------------------------------

    document_search_tool = (
        DocumentSearchTool(
            collection=collection,
            embedding_model=embedding_model,
        )
    )

    # -----------------------------------------------------
    # Configure Together AI
    # -----------------------------------------------------

    llm = LLM(
        model=LLM_MODEL_NAME,
        api_key=api_key,
        temperature=0,
    )

    # -----------------------------------------------------
    # Create Agent
    # -----------------------------------------------------

    hr_agent = Agent(
        role=(
            "Company HR Policy Assistant"
        ),
        goal=(
            "Answer employee questions accurately "
            "using information retrieved from the "
            "company's internal PDF documents."
        ),
        backstory=(
            "You are an HR policy assistant with access "
            "to the company's internal policy documents. "
            "You must search those documents before "
            "answering company-specific questions. "
            "You must never invent policy information."
        ),
        tools=[
            document_search_tool,
        ],
        llm=llm,
        verbose=True,
    )

    # -----------------------------------------------------
    # Create Task
    # -----------------------------------------------------

    policy_task = Task(
        description=(
            "Answer the following employee question:\n\n"
            "{user_question}\n\n"
            "You MUST use the company_document_search "
            "tool before answering.\n\n"
            "Base your answer only on information "
            "retrieved from the company's PDF documents.\n\n"
            "If the retrieved documents do not contain "
            "enough information to answer the question, "
            "clearly state that the information could "
            "not be found in the available documents."
        ),
        expected_output=(
            "A clear and concise answer grounded only "
            "in the retrieved company documents."
        ),
        agent=hr_agent,
    )

    # -----------------------------------------------------
    # Create Crew
    # -----------------------------------------------------

    crew = Crew(
        agents=[
            hr_agent,
        ],
        tasks=[
            policy_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    # -----------------------------------------------------
    # Interactive Loop
    # -----------------------------------------------------

    while True:
        user_question = input(
            "\nAsk an HR policy question: "
        )

        if (
            user_question
            .strip()
            .lower()
            == "exit"
        ):
            break

        result = crew.kickoff(
            inputs={
                "user_question": (
                    user_question
                ),
            }
        )

        print(
            "\n--- FINAL ANSWER ---"
        )

        print(result)


if __name__ == "__main__":
    main()