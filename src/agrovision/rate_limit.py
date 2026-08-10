"""Small in-memory rate limiter for protecting hosted inference credits."""
from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable

from .errors import RateLimitError


class FixedWindowRateLimiter:
    """Limit total requests per process over a rolling time window.

    This is intentionally dependency-free and protects a small portfolio demo from
    accidental bursts. It is not a distributed production gateway; provider quota,
    Render access controls, or an external rate-limiting proxy remain important.
    """

    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
        *,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be at least 1.")
        if window_seconds < 1:
            raise ValueError("window_seconds must be at least 1.")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clock = clock
        self._events: deque[float] = deque()
        self._lock = threading.Lock()

    def check(self) -> None:
        """Record one request or raise a user-safe error when the limit is full."""
        now = self._clock()
        cutoff = now - self.window_seconds
        with self._lock:
            while self._events and self._events[0] <= cutoff:
                self._events.popleft()
            if len(self._events) >= self.max_requests:
                retry_after = max(1, round(self._events[0] + self.window_seconds - now))
                raise RateLimitError(
                    "The demo is receiving too many requests. "
                    f"Retry in about {retry_after} seconds."
                )
            self._events.append(now)

    @property
    def current_count(self) -> int:
        """Return the number of non-expired events for diagnostics/tests."""
        now = self._clock()
        cutoff = now - self.window_seconds
        with self._lock:
            while self._events and self._events[0] <= cutoff:
                self._events.popleft()
            return len(self._events)
