from datetime import datetime
from zoneinfo import ZoneInfo


APP_TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_current_datetime() -> datetime:
    """Return the current application datetime."""
    return datetime.now(APP_TIMEZONE)


def get_temporal_context() -> str:
    """Return current date/time context for the assistant."""

    now = get_current_datetime()

    return (
        f"Current date: {now:%Y-%m-%d}\n"
        f"Current time: {now:%H:%M:%S}\n"
        f"Day: {now:%A}\n"
        f"Timezone: Asia/Kolkata"
    )