from memory_chatbot.llm import LLMClient
from memory_chatbot.memory import MemoryManager


class MemoryChatbot:
    """Chatbot that uses short-term and long-term memory."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.memory = MemoryManager(
            max_short_term_messages=10
        )
        self.llm = LLMClient()

    def build_messages(self, user_message: str) -> list[dict[str, str]]:
        """Build the messages sent to the LLM."""

        relevant_memories = self.memory.retrieve_relevant_memories(
            self.user_id,
            user_message,
        )

        memory_context = ""

        if relevant_memories:
            memory_context = "\n".join(
                f"- {memory['fact']}"
                for memory in relevant_memories
            )

        system_message = (
            "You are a helpful assistant.\n\n"
            "Relevant long-term memories about the user:\n"
            f"{memory_context}"
        )

        messages = [
            {
                "role": "system",
                "content": system_message,
            }
        ]

        messages.extend(
            self.memory.get_short_term_memory()
        )

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        return messages

    def chat(self, user_message: str) -> str:
        """Process a user message and generate a response."""

        messages = self.build_messages(user_message)

        response = self.llm.generate_response(messages)

        self.memory.add_message(
            "user",
            user_message,
        )

        self.memory.add_message(
            "assistant",
            response,
        )

        return response