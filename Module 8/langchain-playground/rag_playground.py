import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_together import ChatTogether
from langchain_huggingface import HuggingFaceEmbeddings



def load_api_key() -> SecretStr:
    """
    Load the Together AI API key from the local .env file.
    """

    env_path = Path(__file__).resolve().parent / ".env"

    load_dotenv(
        dotenv_path=env_path,
    )

    api_key = os.getenv(
        "TOGETHER_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "TOGETHER_API_KEY is not configured."
        )

    return SecretStr(api_key)


def create_documents() -> list[Document]:
    """
    Create sample HR policy documents.

    In a real application, these documents could come from
    PDFs, Word files, databases, or other data sources.
    """

    return [
        Document(
            page_content=(
                "Employees receive 12 casual leave days "
                "per calendar year."
            ),
            metadata={
                "source": "leave_policy",
                "type": "casual_leave",
            },
        ),
        Document(
            page_content=(
                "Employees receive 10 sick leave days "
                "per calendar year."
            ),
            metadata={
                "source": "leave_policy",
                "type": "sick_leave",
            },
        ),
        Document(
            page_content=(
                "Casual leave must be applied at least "
                "one day in advance whenever possible."
            ),
            metadata={
                "source": "leave_policy",
                "type": "casual_leave",
            },
        ),
        Document(
            page_content=(
                "Employees can carry forward a maximum "
                "of 5 unused earned leave days to the "
                "next calendar year."
            ),
            metadata={
                "source": "leave_policy",
                "type": "earned_leave",
            },
        ),
    ]


def format_documents(
    documents: list[Document],
) -> str:
    """
    Convert retrieved LangChain Document objects
    into a single context string for the LLM.
    """

    return "\n\n".join(
        document.page_content
        for document in documents
    )


def main() -> None:
    # ---------------------------------------------------------
    # Step 1: Load configuration
    # ---------------------------------------------------------

    api_key = load_api_key()

    # ---------------------------------------------------------
    # Step 2: Create the source documents
    # ---------------------------------------------------------

    documents = create_documents()

    # ---------------------------------------------------------
    # Step 3: Create the embedding model
    # ---------------------------------------------------------

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ---------------------------------------------------------
    # Step 4: Create the vector store
    # ---------------------------------------------------------

    vector_store = InMemoryVectorStore(
        embedding=embeddings,
    )

    # ---------------------------------------------------------
    # Step 5: Embed and store the documents
    # ---------------------------------------------------------

    vector_store.add_documents(
        documents=documents,
    )

    # ---------------------------------------------------------
    # Step 6: Create the retriever
    # ---------------------------------------------------------

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 2,
        }
    )

    # ---------------------------------------------------------
    # Step 7: Create the RAG prompt
    # ---------------------------------------------------------

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an HR policy assistant.

                Answer the employee's question using only
                the provided context.

                If the answer is not available in the context,
                clearly say that you do not have enough
                information to answer the question.

                Context:

                {context}
                """,
            ),
            (
                "human",
                "{question}",
            ),
        ]
    )

    # ---------------------------------------------------------
    # Step 8: Create the chat model
    # ---------------------------------------------------------

    model = ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        temperature=0,
        api_key=api_key,
    )

    # ---------------------------------------------------------
    # Step 9: Build the complete LCEL RAG pipeline
    # ---------------------------------------------------------

    rag_chain = (
        {
            "context": (
                retriever
                | format_documents
            ),
            "question": RunnablePassthrough(),
        }
        | prompt
        | model
        | StrOutputParser()
    )

    # ---------------------------------------------------------
    # Step 10: Get the user's question
    # ---------------------------------------------------------

    question = input(
        "\nAsk an HR policy question: "
    )

    # ---------------------------------------------------------
    # Step 11: Execute the complete RAG pipeline
    # ---------------------------------------------------------

    answer = rag_chain.invoke(
        question
    )

    # ---------------------------------------------------------
    # Step 12: Display the final answer
    # ---------------------------------------------------------

    print(
        "\n--- ANSWER ---"
    )

    print(
        answer
    )


if __name__ == "__main__":
    main()