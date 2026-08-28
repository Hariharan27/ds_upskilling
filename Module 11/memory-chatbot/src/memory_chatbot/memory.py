from datetime import datetime, timedelta
from typing import Dict, List, Optional


class MemoryManager:
    """Manages short-term and long-term memory for a user."""

    def __init__(
        self,
        max_short_term_messages: int = 10,
        long_term_memory_ttl_days: int = 30,
    ):
        self.max_short_term_messages = max_short_term_messages
        self.long_term_memory_ttl_days = long_term_memory_ttl_days

        # Recent conversation messages
        self.short_term_memory: List[Dict[str, str]] = []

        # Important user facts
        self.long_term_memory: List[Dict] = []


    def add_message(self, role: str, content: str) -> None:
        """Add a message to short-term conversation memory."""

        message = {
            "role": role,
            "content": content,
        }

        self.short_term_memory.append(message)

        # Keep only the most recent N messages.
        if len(self.short_term_memory) > self.max_short_term_messages:
            self.short_term_memory.pop(0)

    def get_short_term_memory(self) -> List[Dict[str, str]]:
        """Return recent conversation history."""

        return self.short_term_memory


    def add_long_term_memory(
        self,
        user_id: str,
        fact: str,
        ttl_days: Optional[int] = None,
    ) -> None:
        """Store an important fact about a user."""

        # IMPORTANT:
        # 0 is a valid TTL, so we must check for None explicitly.
        if ttl_days is None:
            ttl_days = self.long_term_memory_ttl_days

        created_at = datetime.now()
        expires_at = created_at + timedelta(days=ttl_days)

        memory = {
            "user_id": user_id,
            "fact": fact,
            "created_at": created_at,
            "expires_at": expires_at,
        }

        self.long_term_memory.append(memory)

    def get_long_term_memory(self, user_id: str) -> List[Dict]:
        """Retrieve active long-term memories for a user."""

        now = datetime.now()

        return [
            memory
            for memory in self.long_term_memory
            if memory["user_id"] == user_id
            and memory["expires_at"] > now
        ]

 
    def retrieve_relevant_memories(
        self,
        user_id: str,
        query: str,
    ) -> List[Dict]:
        """
        Retrieve relevant memories using simple keyword matching.

        This is intentionally a basic implementation.
        A production system can replace this with embedding/vector
        similarity search.
        """

        stop_words = {
            "a",
            "an",
            "the",
            "is",
            "are",
            "am",
            "as",
            "was",
            "were",
            "what",
            "who",
            "where",
            "when",
            "why",
            "how",
            "does",
            "do",
            "did",
            "user",
            "me",
            "my",
            "i",
            "you",
            "your",
            "to",
            "of",
            "in",
            "on",
            "for",
        }

        query_words = {
            word.strip("?!.,")
            for word in query.lower().split()
            if word.strip("?!.,") not in stop_words
        }

        relevant_memories = []

        for memory in self.get_long_term_memory(user_id):
            fact_words = {
                word.strip("?!.,")
                for word in memory["fact"].lower().split()
                if word.strip("?!.,") not in stop_words
            }

            if query_words.intersection(fact_words):
                relevant_memories.append(memory)

        return relevant_memories


    def consolidate_memory(
        self,
        user_id: str,
        fact: str,
    ) -> bool:
        """
        Store a fact only if an equivalent active memory doesn't exist.

        Returns True when a new memory is stored.
        Returns False when the memory already exists.
        """

        existing_memories = self.get_long_term_memory(user_id)

        for memory in existing_memories:
            if memory["fact"].lower() == fact.lower():
                return False

        self.add_long_term_memory(user_id, fact)

        return True


    def remove_expired_memories(self) -> None:
        """Remove memories whose expiry time has passed."""

        now = datetime.now()

        self.long_term_memory = [
            memory
            for memory in self.long_term_memory
            if memory["expires_at"] > now
        ]