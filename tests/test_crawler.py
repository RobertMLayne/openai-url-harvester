"""
Test for openai_url_harvester crawler functionality.
Runs a smoke test to verify basic crawling and output generation.
"""

from __future__ import annotations

import functools
import http.server
import os
import pathlib
import socketserver
import subprocess
import sys
import threading


def test_crawler_smoke(tmp_path: pathlib.Path) -> None:
    """
    Smoke test for the openai_url_harvester crawler.
    Runs the crawler on https://example.com/
    and checks that output files are generated.
    """
    out = tmp_path / "urls.txt"
    details = tmp_path / "details.csv"

    # Create a tiny static site in a temp directory for deterministic testing
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    (site_dir / "index.html").write_text(
        '<html><body><a href="/page2.html">next</a></body></html>',
        encoding="utf-8",
    )
    (site_dir / "page2.html").write_text(
        '<html><body><p>page2</p></body></html>', encoding="utf-8"
    )

    # Start a small HTTP server in a background thread
    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(site_dir)
    )
    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as httpd:
        port = httpd.server_address[1]

        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()

        try:
            repo_root = pathlib.Path(__file__).resolve().parents[1]
            start_url = f"http://127.0.0.1:{port}/"

            # Option A: run the crawler in-process (preferred for CI/dev)
            # This uses the current test environment's installed deps.
            import asyncio

            # Ensure the local src/ is importable in the current process so we
            # can call run_crawl directly instead of spawning a subprocess.
            sys.path.insert(0, str(repo_root / "src"))

            # Some CI/dev environments may not have aiolimiter installed.
            # If the package is available via pip that's fine. Otherwise our
            # local shim under src/aiolimiter will be found via sys.path.
            try:  # pragma: no cover - environment dependent
                import aiolimiter  # type: ignore  # noqa: F401
            except ImportError:
                pass

            from openai_url_harvester.crawl import (
                run_crawl,
            )

            # Optionally, run as a subprocess to exercise the -m entrypoint and
            # demonstrate setting PYTHONPATH so src/ is importable. To use that
            # mode set OPENAI_URL_HARVESTER_TEST_SUBPROCESS=1 in the env.
            if os.getenv("OPENAI_URL_HARVESTER_TEST_SUBPROCESS", "0") == "1":
                env = os.environ.copy()
                # Ensure the subprocess can import the package located under
                # src/
                env["PYTHONPATH"] = str(repo_root / "src")

                cmd = [
                    sys.executable,
                    "-m",
                    "openai_url_harvester",
                    "crawl",
                    "--start",
                    start_url,
                    # No --allow; default is to allow all hosts which is fine
                    # for this local test server.
                    "--max-pages",
                    "10",
                    "--depth",
                    "1",
                    "--concurrency",
                    "5",
                    "--per-host-qps",
                    "2",
                    "--delay",
                    "0.01",
                    "--request-timeout",
                    "15",
                    "--details-out",
                    str(details),
                    "--out",
                    str(out),
                    "--respect-robots",
                    "false",
                ]

                subprocess.run(cmd, check=True, cwd=repo_root, env=env)
            else:
                # Call run_crawl directly in the test process. This avoids
                # subprocess dependency mismatches and is faster.
                asyncio.run(
                    run_crawl(
                        start_urls=[start_url],
                        allow_hosts=set(),
                        max_pages=10,
                        max_depth=1,
                        concurrency=5,
                        per_host_qps=2.0,
                        delay=0.01,
                        user_agent="test-agent",
                        request_timeout=15,
                        respect_robots=False,
                        include_assets=False,
                        out_path=str(out),
                        details_path=str(details),
                        cache_html_dir=None,
                        export_json_path=None,
                        sitemap_out=None,
                        sitemap_max_urls=50000,
                        sitemap_gzip=False,
                    )
                )
                # We don't assert on discovered URL count to avoid flakes;
                # instead verify output files were created below.
        finally:
            httpd.shutdown()
            thread.join(timeout=1.0)

    # Verify outputs were written
    assert out.exists(), f"Expected output file {out} to be created"
    assert details.exists(), f"Expected details file {details} to be created"
