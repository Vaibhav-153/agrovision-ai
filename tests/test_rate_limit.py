from __future__ import annotations

import pytest

from agrovision.errors import RateLimitError
from agrovision.rate_limit import FixedWindowRateLimiter


def test_rate_limiter_blocks_and_recovers() -> None:
    now = [100.0]
    limiter = FixedWindowRateLimiter(2, 10, clock=lambda: now[0])

    limiter.check()
    limiter.check()
    assert limiter.current_count == 2

    with pytest.raises(RateLimitError, match="too many requests"):
        limiter.check()

    now[0] = 111.0
    limiter.check()
    assert limiter.current_count == 1


def test_rate_limiter_rejects_bad_configuration() -> None:
    with pytest.raises(ValueError):
        FixedWindowRateLimiter(0, 60)
    with pytest.raises(ValueError):
        FixedWindowRateLimiter(1, 0)
