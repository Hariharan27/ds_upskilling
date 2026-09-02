from __future__ import annotations

import hashlib

import redis

from functools import lru_cache
from app.core.config import get_settings


CACHE_VERSION = "v1"
POLICY_CACHE_PREFIX = "employee-assistant:policy"

class RedisCache:
    """Application cache backed by Redis."""

    def __init__(self) -> None:
        settings = get_settings()

        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
            protocol=2,
        )

        self.ttl_seconds = settings.cache_ttl_seconds

    def get(self, key: str) -> str | None:
        """Return a cached value if present."""

        try:
            return self.client.get(key)
        except redis.RedisError:
            return None

    def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
    ) -> None:
        """Store a value with a TTL."""

        try:
            self.client.set(
                key,
                value,
                ex=ttl or self.ttl_seconds,
            )
        except redis.RedisError:
            pass

    def delete(self, key: str) -> None:
        """Delete a specific cache entry."""

        try:
            self.client.delete(key)
        except redis.RedisError:
            pass

    def invalidate_policy_cache(self) -> int:
        """Invalidate all policy-related cache entries."""

        try:
            keys = list(
                self.client.scan_iter(
                    match=f"{POLICY_CACHE_PREFIX}:*",
                )
            )

            if not keys:
                return 0

            return self.client.delete(*keys)

        except redis.RedisError:
            return 0

    def make_router_key(
    self,
    message: str,
    model: str,
    prompt_version: str,
) -> str:
        """Create a cache key for a router decision."""

        value = "|".join(
            [
                message.strip().lower(),
                model,
                prompt_version,
            ]
        )

        return self.make_key("router", value)

    def make_policy_key(
        self,
        question: str,
        model: str,
        prompt_version: str,
        temporal_context: str,
    ) -> str:
        """Create a cache key for a generated policy answer."""

        temporal_lines = temporal_context.splitlines()

        current_date = next(
            (
                line
                for line in temporal_lines
                if line.startswith("Current date:")
            ),
            "",
        )

        timezone = next(
            (
                line
                for line in temporal_lines
                if line.startswith("Timezone:")
            ),
            "",
        )

        value = "|".join(
            [
                question.strip().lower(),
                model,
                prompt_version,
                current_date,
                timezone,
            ]
        )

        return self.make_key("policy", value)

    @staticmethod
    def make_key(
        prefix: str,
        value: str,
    ) -> str:
        """Create a versioned cache key."""

        normalized_value = value.strip().lower()

        digest = hashlib.sha256(
            normalized_value.encode("utf-8")
        ).hexdigest()

        return (
            f"employee-assistant:"
            f"{prefix}:"
            f"{CACHE_VERSION}:"
            f"{digest}"
        )

@lru_cache(maxsize=1)
def get_cache() -> RedisCache:
    """Return the application-wide Redis cache."""

    return RedisCache()