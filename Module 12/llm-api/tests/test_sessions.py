from datetime import datetime, timedelta

from llm_api.sessions import SessionManager


def test_create_session_returns_uuid():
    manager = SessionManager()

    conversation_id = manager.create_session("user_1")

    assert conversation_id in manager.sessions
    assert len(conversation_id) == 36


def test_user_can_access_own_session():
    manager = SessionManager()

    conversation_id = manager.create_session("user_1")

    session = manager.get_session(
        conversation_id,
        "user_1",
    )

    assert session is not None
    assert session["user_id"] == "user_1"


def test_user_cannot_access_another_users_session():
    manager = SessionManager()

    conversation_id = manager.create_session("user_1")

    session = manager.get_session(
        conversation_id,
        "user_2",
    )

    assert session is None


def test_expired_session_is_rejected():
    manager = SessionManager(session_ttl_minutes=30)

    conversation_id = manager.create_session("user_1")

    manager.sessions[conversation_id]["last_accessed"] = (
        datetime.now() - timedelta(minutes=31)
    )

    session = manager.get_session(
        conversation_id,
        "user_1",
    )

    assert session is None
    assert conversation_id not in manager.sessions


def test_cleanup_expired_sessions():
    manager = SessionManager(session_ttl_minutes=30)

    expired_id = manager.create_session("user_1")
    active_id = manager.create_session("user_2")

    manager.sessions[expired_id]["last_accessed"] = (
        datetime.now() - timedelta(minutes=31)
    )

    manager.cleanup_expired_sessions()

    assert expired_id not in manager.sessions
    assert active_id in manager.sessions