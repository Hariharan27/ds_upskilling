import hashlib
import time
import redis
import os

class InMemoryCache:
    """Simple in-memory cache with TTL support."""

    def __init__(self, ttl_seconds: int = 300):
        self._cache = {}
        self.ttl_seconds = ttl_seconds

    def _key(self, prompt: str, model: str) -> str:
        value = f"{model}:{prompt}"
        return hashlib.sha256(value.encode()).hexdigest()

    def get(self, prompt: str, model: str):
        key = self._key(prompt, model)
        entry = self._cache.get(key)

        if entry is None:
            return None

        response, created_at = entry

        if time.time() - created_at >= self.ttl_seconds:
            del self._cache[key]
            return None

        return response

    def set(self, prompt: str, model: str, response: str) -> None:
        key = self._key(prompt, model)
        self._cache[key] = (response, time.time())


class RedisCache:
    """Redis-backed cache for LLM responses."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        password: str | None = None,
        ttl_seconds: int = 300,
    ):
        self.client = redis.Redis(
            host=host or os.getenv("REDIS_HOST", "localhost"),
            port=port or int(os.getenv("REDIS_PORT", "6380")),
            password=password or os.getenv("REDIS_AUTH"),
            decode_responses=True,
        )
        self.ttl_seconds = ttl_seconds

    def _key(self, prompt: str, model: str) -> str:
        value = f"{model}:{prompt}"
        return hashlib.sha256(value.encode()).hexdigest()

    def get(self, prompt: str, model: str):
        key = self._key(prompt, model)
        return self.client.get(key)

    def set(self, prompt: str, model: str, response: str) -> None:
        key = self._key(prompt, model)
        self.client.setex(
            key,
            self.ttl_seconds,
            response,
        )