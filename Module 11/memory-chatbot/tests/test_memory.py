from datetime import datetime, timedelta

from memory_chatbot.memory import MemoryManager


def test_add_message():
    memory = MemoryManager()

    memory.add_message("user", "Hello")

    messages = memory.get_short_term_memory()

    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"


def test_short_term_buffer_window():
    memory = MemoryManager(max_short_term_messages=3)

    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Message 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Message 4")

    messages = memory.get_short_term_memory()

    assert len(messages) == 3
    assert messages[0]["content"] == "Message 2"
    assert messages[-1]["content"] == "Message 4"


def test_add_and_retrieve_long_term_memory():
    memory = MemoryManager()

    memory.add_long_term_memory(
        "user_1",
        "User is a GenAI developer",
    )

    memories = memory.get_long_term_memory("user_1")

    assert len(memories) == 1
    assert memories[0]["fact"] == "User is a GenAI developer"


def test_user_memory_isolation():
    memory = MemoryManager()

    memory.add_long_term_memory(
        "user_1",
        "User 1 works with Python",
    )

    memory.add_long_term_memory(
        "user_2",
        "User 2 works with Java",
    )

    user_1_memories = memory.get_long_term_memory("user_1")

    assert len(user_1_memories) == 1
    assert user_1_memories[0]["fact"] == "User 1 works with Python"


def test_retrieve_relevant_memories():
    memory = MemoryManager()

    memory.add_long_term_memory(
        "user_1",
        "User works as a GenAI developer",
    )

    memory.add_long_term_memory(
        "user_1",
        "User likes cricket",
    )

    memories = memory.retrieve_relevant_memories(
        "user_1",
        "What does the user do as a developer?",
    )

    assert len(memories) == 1
    assert memories[0]["fact"] == "User works as a GenAI developer"


def test_memory_consolidation_prevents_duplicates():
    memory = MemoryManager()

    first_insert = memory.consolidate_memory(
        "user_1",
        "User's name is Hari",
    )

    second_insert = memory.consolidate_memory(
        "user_1",
        "User's name is Hari",
    )

    memories = memory.get_long_term_memory("user_1")

    assert first_insert is True
    assert second_insert is False
    assert len(memories) == 1


def test_expired_memory_is_not_retrieved():
    memory = MemoryManager()

    memory.add_long_term_memory(
        "user_1",
        "Temporary fact",
        ttl_days=0,
    )

    memories = memory.get_long_term_memory("user_1")

    assert len(memories) == 0


def test_remove_expired_memories():
    memory = MemoryManager()

    memory.add_long_term_memory(
        "user_1",
        "Temporary fact",
        ttl_days=0,
    )

    memory.remove_expired_memories()

    assert len(memory.long_term_memory) == 0