# openai-url-harvester Copilot Instructions

## Project Architecture

This is an async web crawler specifically designed for OpenAI documentation sites. Key components:

- **Entry point**: `src/openai_url_harvester/__main__.py` - CLI with `crawl` and `extract` commands
- **Core crawler**: `src/openai_url_harvester/crawl.py` - Async crawler with robots.txt compliance, rate limiting, and CSV export
- **Local extraction**: `src/openai_url_harvester/extract.py` - Extract URLs from local files (HTML, PDF, text)
- **Utilities**: `src/openai_url_harvester/utils.py` - URL normalization and host filtering
- **Sitemap**: `src/openai_url_harvester/sitemap.py` - XML sitemap generation

## Development Workflow

**Setup (PowerShell 7 required):**
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

**Testing:**
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**Run crawl example:**
```powershell
.\.venv\Scripts\python.exe -m openai_url_harvester crawl --start @(Get-Content .\seed_urls.txt) --allow @(Get-Content .\allowlist.txt) --depth 3
```

## Project-Specific Patterns

- **Async concurrency**: Uses `aiohttp` + `aiolimiter` for per-host rate limiting (default 2 QPS)
- **Robots.txt compliance**: RFC 9309 implementation in `RobotsCache` class with proper unavailable vs unreachable handling
- **PowerShell-first**: All CLI examples use PowerShell 7 syntax with `@(Get-Content)` for file reading
- **Data flow**: Crawl → CSV details → URL list → sitemap XML export
- **Content filtering**: Only crawls `text/html` and `application/xhtml+xml` content types
- **URL normalization**: Drops fragments, handles relative URLs, filters by scheme (HTTP/HTTPS only)

## Key Files

- `seed_urls.txt` - Starting URLs for crawl
- `allowlist.txt` - Allowed domains (subdomain matching)
- `PROJECT_INSTRUCTIONS.md` - Mission-critical project context
- Tests use local HTTP server for deterministic crawling

When modifying crawler logic, always preserve robots.txt compliance and rate limiting. Use dataclasses for structured data and maintain async/await patterns throughout.

## Rate Limiting Strategy

Default **2 QPS per host** with added **client-side delay (250 ms)** keeps steady load and smooths burstiness beyond connector concurrency. Conservative crawl rates align with ops guidance (AWS suggests **1 rps** unless coordinated).

**Tuning table:**
- Durable CDNs: raise to 4-8 QPS after monitoring
- Fragile hosts: lower to 0.5-1 QPS
- Use `--per-host-qps` and `--delay` flags for adjustment

Follows REP (RFC 9309) for robots handling and caching to ensure standards alignment.

## Testing Approach

**Two-layer strategy:**

1. **Unit tests**: Mock `aiohttp` with `aioresponses` to assert retry paths, redirects, content-type gates, and robots fallbacks. Uses `pytest-asyncio` for coroutines. Note: `aioresponses` supports **aiohttp < 4.0**.

2. **Integration tests**: Local server via `http.server` or `pytest-httpserver` serves fixtures for 2xx/3xx/4xx/5xx, slow responses, and malformed HTML/PDF.

**Golden crawls**: Use deterministic HTML fixtures and snapshot emitted CSV/URL lists for regression testing.

## Error Handling Patterns

**Robots.txt RFC 9309 compliance:**
- *Unavailable* (4xx): crawling **may proceed**
- *Unreachable* (5xx/timeouts): **treat as disallow**
- Follow up to **5 redirects** for robots fetch
- Cache robots up to **24h** using HTTP caching

**Fetch layer**: Timeouts per request, classify by status class, backoff on repeated 5xx from same host, gate by `Content-Type`. Uses `aiohttp.ClientTimeout` and connector settings.

## File Organization & Cache Layout

**Cache naming**: Percent-encode unsafe bytes, hash full URL to stable filename (or wget-style mapping). Keep **one file per URL** plus sidecar metadata JSON (status, content-type, fetched-at). Reference sitemap output location and schema.

## Dependencies & Version Notes

- **aiolimiter**: Optional; code falls back to internal QPS gate. When present, prefer `AsyncLimiter` per-host
- **Beautiful Soup**: Prefer `lxml` parser for speed, `html5lib` for tolerance. Use `Tag.get()` for attributes. Output may differ by parser; tests must pin parser choice.
- **PDF extraction**: Uses `pdfminer.six.high_level.extract_text`, handle parser errors
- **Testing caveat**: `aioresponses` supports **aiohttp >= 3.3, < 4.0** - pin or adjust on upgrades

## Copilot Configuration

### Scope and Precedence
- `.github/copilot-instructions.md` applies to **all chats** in this workspace
- `*.instructions.md` can be scoped with `applyTo:` frontmatter for specific file patterns
- Order isn't guaranteed; custom instructions do **not** affect inline completions

### Prompt Files Usage
Enable `github.copilot.chat.promptFiles: true` in settings. Store in `.github/prompts/` and invoke via `/name`. Prompt files are on-demand and can live in user profile for cross-workspace reuse.

### Custom Chat Modes
Create `.chatmode.md` files with preselected tools and instructions. Use modes for persistent workflows, prompt files for one-off tasks. Feature is in preview.

### Agent-Mode Tools
**Safe for this repo**: file reading, semantic search, terminal (read-only commands), testing
**Restrict**: file editing without review, external network calls during crawls
Disable tools when running production crawls to prevent interference.

## Security and PII Policy

**Never paste**: secrets, tokens, user data, or private URLs into prompts. Use scrubbed artifacts and example data. Applies to instructions, prompt files, and chat modes.

## Politeness Limits

**Hard caps** (make explicit in all modes):
- `--per-host-qps 2.0` (default), raise to 4-8 for CDNs, lower to 0.5-1 for fragile hosts
- `--delay 0.25` (minimum client-side delay)
- `--concurrency 20` (max concurrent connections)
- Response byte cap: 60KB per fetch to prevent memory issues

## Retry and Backoff

**Status handling**: Exponential backoff for 5xx errors, classify by status class, immediate retry for connection drops. **Robots fetch**: up to 5 redirects, 24h cache TTL, treat 5xx as disallow per RFC 9309.

## Test Matrix

**Supported versions**:
- `aiohttp >= 3.3, < 4.0` (aioresponses constraint)
- `pytest-asyncio >= 0.21`
- `aioresponses >= 0.7.3`

**Golden crawls**: Snapshot CSV/URL outputs as acceptance tests for regression detection.

## Runbook

**Development commands:**
```powershell
# PowerShell 7
.\.venv\Scripts\python.exe -m pytest -q                    # Tests
.\.venv\Scripts\python.exe -m mypy src/                     # Type check
.\.venv\Scripts\python.exe -m ruff check src/              # Lint

# Bash equivalent
./.venv/bin/python -m pytest -q
./.venv/bin/python -m mypy src/
./.venv/bin/python -m ruff check src/
```

**Prompt usage**: `/azure-best-practices`, `/explain-code`
**Mode switching**: Chat → Configure Chat → Modes

## Community Resources

See [Awesome Copilot Customizations](https://github.com/github/awesome-copilot) for vetted examples and patterns.

## Contribution Checklist

PRs changing crawler behavior must:
- Update instructions if limits change
- Add/refresh test fixtures
- Run prompt/mode smoke tests
- Provide both PowerShell and Bash examples
