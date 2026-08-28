from memory_chatbot.app import MemoryChatbot


class FakeLLMClient:
    """Fake LLM client used for testing."""

    def generate_response(self, messages):
        return "This is a fake response."


def test_build_messages_includes_long_term_memory():
    chatbot = MemoryChatbot.__new__(MemoryChatbot)

    chatbot.user_id = "user_1"

    from memory_chatbot.memory import MemoryManager

    chatbot.memory = MemoryManager()
    chatbot.llm = FakeLLMClient()

    chatbot.memory.add_long_term_memory(
        "user_1",
        "User is a GenAI developer",
    )

    messages = chatbot.build_messages(
        "What type of developer is the user?"
    )

    system_message = messages[0]

    assert system_message["role"] == "system"
    assert "User is a GenAI developer" in system_message["content"]


def test_build_messages_includes_short_term_memory():
    chatbot = MemoryChatbot.__new__(MemoryChatbot)

    chatbot.user_id = "user_1"

    from memory_chatbot.memory import MemoryManager

    chatbot.memory = MemoryManager()
    chatbot.llm = FakeLLMClient()

    chatbot.memory.add_message(
        "user",
        "My name is Hari",
    )

    chatbot.memory.add_message(
        "assistant",
        "Nice to meet you, Hari!",
    )

    messages = chatbot.build_messages(
        "What is my name?"
    )

    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "My name is Hari"

    assert messages[2]["role"] == "assistant"
    assert messages[2]["content"] == "Nice to meet you, Hari!"


def test_build_messages_includes_current_user_message():
    chatbot = MemoryChatbot.__new__(MemoryChatbot)

    chatbot.user_id = "user_1"

    from memory_chatbot.memory import MemoryManager

    chatbot.memory = MemoryManager()
    chatbot.llm = FakeLLMClient()

    messages = chatbot.build_messages(
        "What is my name?"
    )

    assert messages[-1]["role"] == "user"
    assert messages[-1]["content"] == "What is my name?"