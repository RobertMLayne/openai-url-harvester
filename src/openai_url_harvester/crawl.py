"""
Concurrent web crawler for openai-url-harvester.
Handles robots.txt, rate limiting, HTML extraction, and sitemap export.
"""

from __future__ import annotations

import json
import asyncio
import csv
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import aiohttp
from aiohttp import ClientTimeout
from aiolimiter import AsyncLimiter
from bs4 import BeautifulSoup

from .sitemap import write_sitemap_auto
from .utils import OK_CONTENT_TYPES, host_ok, is_probably_html, norm_url

DEFAULT_UA = "openai-url-harvester/0.7 (+https://example.invalid)"


@dataclass(slots=True)
class RobotsState:
    """Cached robots.txt policy for a host."""

    mode: str  # "ok", "allow_all", "disallow_all"
    parser: RobotFileParser | None  # RobotFileParser or None


class RobotsCache:
    """Fetch and cache robots.txt per RFC 9309 (unavailable vs unreachable)."""

    def __init__(self, session: aiohttp.ClientSession, user_agent: str):
        self.session = session
        self.user_agent = user_agent
        self._cache: dict[str, RobotsState] = {}

    async def allowed(self, url: str) -> bool:
        """
        Check if the given URL is allowed to be crawled according
        to robots.txt rules. Returns True if allowed, False otherwise.
        """
        host = urlparse(url).netloc
        state = self._cache.get(host)
        if state is None:
            state = await self._load(host, url)
            self._cache[host] = state

        if state.mode == "allow_all":
            return True
        if state.mode == "disallow_all":
            return False
        # state.mode == "ok"
        assert state.parser is not None
        return state.parser.can_fetch(self.user_agent, url)

    async def _load(self, host: str, url_for_scheme: str) -> RobotsState:
        robots_url = f"{urlparse(url_for_scheme).scheme}://{host}/robots.txt"
        try:
            async with self.session.get(
                robots_url, timeout=ClientTimeout(total=15)
            ) as r:
                status = r.status
                txt = await r.text(errors="ignore")
        except (aiohttp.ClientError, asyncio.TimeoutError):
            # Unreachable => MUST assume complete disallow (RFC 9309 §2.3.1.4).
            return RobotsState(mode="disallow_all", parser=None)

        if 500 <= status <= 599:
            # Unreachable (server error) => disallow all.
            return RobotsState(mode="disallow_all", parser=None)
        if 400 <= status <= 499:
            # Unavailable => may access any resources.
            return RobotsState(mode="allow_all", parser=None)

        rp = RobotFileParser()
        rp.parse(txt.splitlines())
        return RobotsState(mode="ok", parser=rp)

    # Public wrapper for external use (non-protected API)
    async def load(self, host: str, url_for_scheme: str | None) -> RobotsState:
        """
        Public API: load robots for host. If url_for_scheme is None,
        assume https://{host}/ as a fallback to determine scheme.
        This also caches the loaded RobotsState so callers don't need to
        call the protected _load method directly.
        """
        if url_for_scheme is None:
            url_for_scheme = f"https://{host}/"
        # Use cached value if present
        state = self._cache.get(host)
        if state is None:
            state = await self._load(host, url_for_scheme)
            self._cache[host] = state
        return state


async def _fetch_html(
    session: aiohttp.ClientSession, url: str, timeout: ClientTimeout
) -> tuple[int | None, str | None, str]:
    try:
        async with session.get(url, timeout=timeout) as r:
            ct = r.headers.get("content-type", "")
            text = (
                await r.text(errors="ignore")
                if any(t in (ct or "") for t in OK_CONTENT_TYPES)
                else ""
            )
            return r.status, ct, text
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None, None, ""


async def run_crawl(
    start_urls: Iterable[str],
    allow_hosts: set[str],
    max_pages: int,
    max_depth: int | None,
    concurrency: int,
    per_host_qps: float,
    delay: float,
    user_agent: str,
    request_timeout: int,
    respect_robots: bool,
    include_assets: bool,
    out_path: str,
    details_path: str | None,
    cache_html_dir: str | None,
    export_json_path: str | None,
    sitemap_out: str | None,
    sitemap_max_urls: int,
    sitemap_gzip: bool,
) -> list[str]:
    """
    Concurrent crawl with per-host rate limiting,
    optional robots, and optional sitemap export.
    """

    visited: set[str] = set()
    enqueued: set[str] = set()

    q: asyncio.Queue[tuple[str, int, str | None]] = asyncio.Queue()
    for u in start_urls:
        q.put_nowait((u, 0, None))
        enqueued.add(u)

    timeout = ClientTimeout(total=request_timeout)
    connector = aiohttp.TCPConnector(limit=0)
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1",
    }

    async with aiohttp.ClientSession(
        timeout=timeout, connector=connector, headers=headers
    ) as session:
        robots = RobotsCache(session, user_agent)

        # Prefetch robots.txt for all hosts in start_urls
        hosts_to_prefetch = {urlparse(u).netloc for u in start_urls}
        await asyncio.gather(
            *(
                robots.load(
                    host,
                    next(
                        (u for u in start_urls if urlparse(u).netloc == host),
                        None,
                    ),
                )
                for host in hosts_to_prefetch
            )
        )

        # CSV details
        detf = None
        writer = None
        if details_path:
            os.makedirs(os.path.dirname(details_path), exist_ok=True)
            detf = open(details_path, "w", encoding="utf-8", newline="")
            writer = csv.writer(detf)
            writer.writerow(
                [
                    "url",
                    "referrer",
                    "status",
                    "content_type",
                    "depth",
                    "discovered_at",
                ]
            )

        host_limiters: dict[str, AsyncLimiter] = defaultdict(
            lambda: AsyncLimiter(per_host_qps, 1)
        )
        sem = asyncio.Semaphore(concurrency)

        async def worker() -> None:
            while len(visited) < max_pages:
                try:
                    url, depth, ref = await asyncio.wait_for(
                        q.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    if q.empty():
                        break
                    continue

                if url in visited:
                    q.task_done()
                    continue
                if not host_ok(urlparse(url).netloc, allow_hosts):
                    q.task_done()
                    continue
                if respect_robots and not await robots.allowed(url):
                    q.task_done()
                    continue

                host = urlparse(url).netloc
                limiter = host_limiters[host]

                async with sem:
                    async with limiter:
                        await asyncio.sleep(delay)
                        # Ensure variables are always bound so downstream use
                        # (e.g. writer.writerow) cannot see them as possibly
                        # unbound.
                        status: int | None = None
                        ct: str | None = None
                        text: str = ""
                        status, ct, text = await _fetch_html(
                            session, url, timeout
                        )

                visited.add(url)
                if writer:
                    writer.writerow(
                        [
                            url,
                            ref or "",
                            status if status is not None else "",
                            ct or "",
                            depth,
                            datetime.now(timezone.utc).isoformat(),
                        ]
                    )

                # Ensure status is not None before numeric comparison to avoid
                # potential "possibly unbound" / type-checker warnings.
                if status is not None and status < 400 and text:
                    if cache_html_dir:
                        os.makedirs(cache_html_dir, exist_ok=True)
                        fname = (
                            url.replace("https://", "")
                            .replace("http://", "")
                            .replace("/", "__")
                            + ".html"
                        )
                        with open(
                            os.path.join(cache_html_dir, fname),
                            "w",
                            encoding="utf-8",
                            errors="ignore",
                        ) as hf:
                            hf.write(text)

                    soup = BeautifulSoup(text, "html.parser")
                    links: list[str] = []
                    for tag, attr in (
                        ("a", "href"),
                        ("link", "href"),
                        ("script", "src"),
                        ("img", "src"),
                    ):
                        for t in soup.find_all(tag):
                            href = t.get(attr)
                            # Ensure href is a string or None
                            if isinstance(href, list):
                                href = href[0] if href else None
                            elif not (isinstance(href, str) or href is None):
                                href = str(href)
                            u2 = norm_url(url, href)
                            if u2:
                                links.append(u2)

                    if not include_assets:
                        links = [u for u in links if is_probably_html(u)]

                    for u2 in links:
                        if (
                            u2 not in enqueued
                            and host_ok(urlparse(u2).netloc, allow_hosts)
                            and (
                                (max_depth is None) or (depth + 1 <= max_depth)
                            )
                        ):
                            enqueued.add(u2)
                            q.put_nowait((u2, depth + 1, url))

                q.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(concurrency)]
        await q.join()
        for w in workers:
            w.cancel()
        if detf:
            detf.close()

    unique_sorted = sorted(visited)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as outf:
        outf.write("\n".join(unique_sorted))

    if export_json_path:

        os.makedirs(os.path.dirname(export_json_path) or ".", exist_ok=True)
        with open(export_json_path, "w", encoding="utf-8") as jf:
            json.dump(
                {"urls": unique_sorted}, jf, ensure_ascii=False, indent=2
            )

    if sitemap_out:
        write_sitemap_auto(
            unique_sorted,
            sitemap_out,
            max_urls=sitemap_max_urls,
            gzip_output=sitemap_gzip,
        )

    return unique_sorted
