"""
Utilities for URL normalization, host filtering, and HTML heuristics.
Provides helpers for working with URLs and content types in crawling.
"""

from __future__ import annotations

from html import unescape
from urllib.parse import urljoin, urldefrag, urlparse
import os

OK_CONTENT_TYPES: tuple[str, ...] = (
    "text/html",
    "application/xhtml+xml",
)


def norm_url(base: str, href: str | None) -> str | None:
    """Normalize href to absolute, drop fragments and non-HTTP(S)."""
    if not href:
        return None
    href = unescape(href.strip())
    abs_u = urljoin(base, href)
    abs_u, _ = urldefrag(abs_u)
    p = urlparse(abs_u)
    if p.scheme not in ("http", "https"):
        return None
    return abs_u


def host_ok(host: str, allow_hosts: set[str]) -> bool:
    """True if host is empty or suffix-matches any domain in allowlist."""
    if not allow_hosts:
        return True
    host = host.lower()
    return any(host == a or host.endswith("." + a) for a in allow_hosts)


def is_probably_html(url: str) -> bool:
    """Heuristic: keep URLs with no extension or common HTML ones."""
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    return ext in ("", ".html", ".htm", ".xhtml")
