from datetime import datetime, timedelta
from uuid import uuid4


class SessionManager:
    """Manages conversation sessions."""

    def __init__(self, session_ttl_minutes: int = 30):
        self.session_ttl_minutes = session_ttl_minutes
        self.sessions = {}

    def create_session(self, user_id: str) -> str:
        """Create a new conversation session."""

        conversation_id = str(uuid4())

        self.sessions[conversation_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
        }

        return conversation_id

    def get_session(
        self,
        conversation_id: str,
        user_id: str,
    ):
        """Retrieve a session belonging to the specified user."""

        session = self.sessions.get(conversation_id)

        if session is None:
            return None

        # Multi-tenant isolation.
        if session["user_id"] != user_id:
            return None

        # Session expiry.
        expiry_time = session["last_accessed"] + timedelta(
            minutes=self.session_ttl_minutes
        )

        if datetime.now() >= expiry_time:
            del self.sessions[conversation_id]
            return None

        session["last_accessed"] = datetime.now()

        return session

    def cleanup_expired_sessions(self) -> None:
        """Remove expired sessions."""

        now = datetime.now()

        expired_ids = []

        for conversation_id, session in self.sessions.items():
            expiry_time = session["last_accessed"] + timedelta(
                minutes=self.session_ttl_minutes
            )

            if now >= expiry_time:
                expired_ids.append(conversation_id)

        for conversation_id in expired_ids:
            del self.sessions[conversation_id]