from langchain_core.output_parsers import StrOutputParser

from app.ai.prompts.rag import RAG_PROMPT
from app.ai.models.chat import get_chat_model

def generate_answer(
        question:str,
        context: str,

)->str:
    model = get_chat_model()

    chain  = RAG_PROMPT | model | StrOutputParser()

    return chain.invoke({"context": context, "question": question})