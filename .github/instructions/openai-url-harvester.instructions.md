---
applyTo: "**/*.py,**/pyproject.toml,**/requirements.txt,**/seed_urls.txt,**/allowlist.txt"
description: "OpenAI URL harvester development rules"
---

# OpenAI URL Harvester Instructions

## Core Principles

- **Async-first**: Maintain `aiohttp` + `aiolimiter` patterns for concurrent crawling
- **RFC 9309 compliance**: Preserve robots.txt handling with proper unavailable vs unreachable logic
- **Rate limiting**: Default 2 QPS per host with 250ms client delay for politeness
- **PowerShell examples**: All CLI examples use PowerShell 7 syntax with `@(Get-Content)`

## Code Patterns

- Use `dataclasses` for structured data (CrawlResult, RobotsState, etc.)
- Maintain async/await throughout the pipeline
- Gate content by MIME type: only `text/html` and `application/xhtml+xml`
- URL normalization: drop fragments, filter by scheme (HTTP/HTTPS only)

## Testing Standards

- Unit tests: Mock `aiohttp` with `aioresponses` (supports aiohttp < 4.0)
- Integration tests: Local HTTP server for deterministic crawling
- Golden crawls: Snapshot CSV/URL outputs for regression detection

## Development Workflow

```powershell
# Setup
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .

# Test
.\.venv\Scripts\python.exe -m pytest -q

# Crawl example
.\.venv\Scripts\python.exe -m openai_url_harvester crawl `
  --start @(Get-Content .\seed_urls.txt) `
  --allow @(Get-Content .\allowlist.txt) `
  --depth 3
```

## Politeness Limits

**Hard caps** (enforce in all modes):
- `--per-host-qps 2.0` (default), raise to 4-8 for CDNs, lower to 0.5-1 for fragile hosts
- `--delay 0.25` (minimum client-side delay)
- `--concurrency 20` (max concurrent connections)
- Response byte cap: 60KB per fetch
