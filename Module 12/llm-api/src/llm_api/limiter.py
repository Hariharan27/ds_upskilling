from collections import defaultdict
from datetime import datetime, timedelta


class RateLimiter:
    """Simple in-memory per-user rate limiter."""

    def __init__(
        self,
        max_requests: int = 5,
        window_seconds: int = 60,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self.requests = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        """Return True when the user is within the rate limit."""

        now = datetime.now()
        window_start = now - timedelta(
            seconds=self.window_seconds
        )

        # Keep only requests inside the current window.
        self.requests[user_id] = [
            timestamp
            for timestamp in self.requests[user_id]
            if timestamp > window_start
        ]

        if len(self.requests[user_id]) >= self.max_requests:
            return False

        self.requests[user_id].append(now)

        return True