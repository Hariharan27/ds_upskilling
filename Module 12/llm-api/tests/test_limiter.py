from llm_api.limiter import RateLimiter


def test_requests_are_allowed_within_limit():
    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.is_allowed("user_1") is True
    assert limiter.is_allowed("user_1") is True
    assert limiter.is_allowed("user_1") is True


def test_request_is_rejected_after_limit():
    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.is_allowed("user_1") is True
    assert limiter.is_allowed("user_1") is True
    assert limiter.is_allowed("user_1") is True

    assert limiter.is_allowed("user_1") is False


def test_users_have_separate_limits():
    limiter = RateLimiter(
        max_requests=2,
        window_seconds=60,
    )

    assert limiter.is_allowed("user_1") is True
    assert limiter.is_allowed("user_1") is True
    assert limiter.is_allowed("user_1") is False

    assert limiter.is_allowed("user_2") is True