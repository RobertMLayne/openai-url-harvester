"""Tiny shim of aiolimiter.AsyncLimiter used for tests and CI when the
real package is not installed. This intentionally implements a no-op
async context manager with the same constructor signature used by the
crawler. It's lightweight and should be safe in CI/dev test runs.
"""

from __future__ import annotations

from typing import Any


class AsyncLimiter:
    """Minimal async context manager shim for rate limiting.

    Usage in production code expects AsyncLimiter(rate, burst). The shim
    accepts any args/kwargs and is awaitable via async with.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        del args, kwargs

    async def __aenter__(self) -> "AsyncLimiter":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        del exc_type, exc, tb
        return False
