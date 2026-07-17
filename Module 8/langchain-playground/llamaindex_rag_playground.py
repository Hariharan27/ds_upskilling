import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.chat_models.litellm_router import model_extra_key_name
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.core import (
    Document,
    Settings,
    VectorStoreIndex,
)
from llama_index.core.base.embeddings.base import similarity
from llama_index.core.tools import query_engine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.together import TogetherLLM

def load_api_key() -> str:
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

    return api_key

def create_documents() -> list[Document]:
    """
    Create sample HR policy documents.
    """

    return [
        Document(
            text=(
                "Employees receive 12 casual leave days "
                "per calendar year."
            ),
            metadata={
                "source": "leave_policy",
                "type": "casual_leave",
            },
        ),
        Document(
            text=(
                "Employees receive 10 sick leave days "
                "per calendar year."
            ),
            metadata={
                "source": "leave_policy",
                "type": "sick_leave",
            },
        ),
        Document(
            text=(
                "Casual leave must be applied at least "
                "one day in advance whenever possible."
            ),
            metadata={
                "source": "leave_policy",
                "type": "casual_leave",
            },
        ),
        Document(
            text=(
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

def main()->None:

    api_key = load_api_key()

    Settings.embed_model = HuggingFaceEmbedding(
        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        )
    )


    Settings.llm = TogetherLLM(
        model= (
            "meta-llama/"
            "Llama-3.3-70B-Instruct-Turbo"
        ),
        api_key=api_key,
        temperature=0.0
    )

    documents = create_documents()


    index = VectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine(
        similarity_top_k=2,
    )

    while True:
        question = input("Ask your question: ")

        if question.lower() == "exit":
            break

        response = query_engine.query(question)

        print(
            "\n--- ANSWER ---"
        )

        print(response)

        print(
            "\n--- SOURCE NODES ---"
        )

        for source_node in response.source_nodes:
            print(
                "\nScore:",
                source_node.score,
            )

            print(
                "Text:",
                source_node.node.get_content(),
            )

            print(
                "Metadata:",
                source_node.node.metadata,
            )


if __name__ == "__main__":
    main()







