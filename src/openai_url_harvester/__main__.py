"""
Main entry point for openai_url_harvester CLI.
Provides commands for crawling and extracting URLs.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from typing import Sequence


# Third-party imports (if needed in this file)
# import aiohttp
# from aiohttp import ClientTimeout
# from aiolimiter import AsyncLimiter
# from bs4 import BeautifulSoup

from .crawl import run_crawl, DEFAULT_UA
from .extract import extract_from_files, save_json, save_list


def _bool(v: str) -> bool:
    return str(v).lower() in {"1", "true", "t", "yes", "y", "on"}


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the argument parser for the openai_url_harvester CLI.
    """
    p = argparse.ArgumentParser(prog="openai_url_harvester")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("crawl", help="Crawl the web starting from seed URLs")
    c.add_argument("--start", nargs="+", required=True, help="Seed URLs")
    c.add_argument(
        "--allow",
        nargs="*",
        default=[],
        help="Allowed domains (subdomains allowed)",
    )
    c.add_argument("--max-pages", type=int, default=5000)
    c.add_argument("--depth", type=int, default=None)
    c.add_argument("--concurrency", type=int, default=20)
    c.add_argument("--per-host-qps", type=float, default=2.0)
    c.add_argument("--delay", type=float, default=0.25)
    c.add_argument("--request-timeout", type=int, default=30)
    c.add_argument("--user-agent", default=DEFAULT_UA)
    c.add_argument(
        "--respect-robots",
        type=str,
        default="true",
        help="true/false (RFC 9309 rules)",
    )
    c.add_argument(
        "--include-assets",
        type=str,
        default="false",
        help="true/false include non-HTML assets in frontier",
    )
    c.add_argument(
        "--out", required=True, help="Write discovered URL list here"
    )
    c.add_argument("--details-out", default=None, help="CSV of crawl events")
    c.add_argument(
        "--cache-html", default=None, help="Directory to cache HTML"
    )
    c.add_argument(
        "--export-json", default=None, help="Write JSON dump of URLs"
    )

    # Sitemap options (auto-chunk and optional gzip)
    c.add_argument(
        "--sitemap-out", default=None, help="Path to sitemap.xml or index"
    )
    c.add_argument(
        "--sitemap-max-urls",
        type=int,
        default=50000,
        help="Max URLs per sitemap file (spec default 50,000)",
    )
    c.add_argument(
        "--sitemap-gzip",
        type=str,
        default="false",
        help="true/false gzip sitemap files",
    )

    e = sub.add_parser("extract", help="Extract URLs from local files")
    e.add_argument(
        "--path", nargs="+", required=True, help="Files or directories"
    )
    e.add_argument("--out", required=True)
    e.add_argument("--json-out", default=None)

    return p


def main(argv: Sequence[str] | None = None) -> None:
    """
    Main CLI entry point for openai_url_harvester.
    Parses arguments and dispatches to crawl or extract logic.
    """
    args = build_parser().parse_args(argv)

    if args.cmd == "crawl":
        urls = asyncio.run(
            run_crawl(
                start_urls=args.start,
                allow_hosts=set(a.lower() for a in args.allow),
                max_pages=args.max_pages,
                max_depth=args.depth,
                concurrency=args.concurrency,
                per_host_qps=args.per_host_qps,
                delay=args.delay,
                user_agent=args.user_agent,
                request_timeout=args.request_timeout,
                respect_robots=_bool(args.respect_robots),
                include_assets=_bool(args.include_assets),
                out_path=args.out,
                details_path=args.details_out,
                cache_html_dir=args.cache_html,
                export_json_path=args.export_json,
                sitemap_out=args.sitemap_out,
                sitemap_max_urls=args.sitemap_max_urls,
                sitemap_gzip=_bool(args.sitemap_gzip),
            )
        )
        print(f"Wrote {len(urls)} URLs to {args.out}", file=sys.stderr)

    elif args.cmd == "extract":
        urls = extract_from_files(args.path)
        save_list(urls, args.out)
        if args.json_out:
            save_json(urls, args.json_out)
        print(f"Wrote {len(urls)} URLs to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
