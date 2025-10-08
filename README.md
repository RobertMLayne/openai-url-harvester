# openai-url-harvester v7

Async crawler + local extractor with robots.txt support, depth limits, per-host QPS, CSV details, and sitemap export.

## Quickstart (PowerShell 7)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e .

# Crawl seeds from files and export sitemap
.\.venv\Scripts\python.exe -m openai_url_harvester crawl `
  --start @(Get-Content .\seed_urls.txt) `
  --allow @(Get-Content .\allowlist.txt) `
  --depth 3 --max-pages 5000 `
  --concurrency 20 --per-host-qps 4 --delay 0.25 `
  --details-out artifacts\crawl_details.csv --out artifacts\urls.txt `
  --sitemap-out artifacts\sitemap.xml --cache-html cache `
  --respect-robots true --export-json artifacts\urls.json

# Extract URLs from local files
.\.venv\Scripts\python.exe -m openai_url_harvester extract `
  --path . `
  --out artifacts\extracted_urls.txt
```

## Flags

- `--respect-robots {true|false}`: default true.
- `--cache-html DIR`: save fetched HTML.
- `--sitemap-out PATH`: write sitemap.
- `--export-json PATH`: JSON dump of visited URLs.
- `--include-assets {true|false}`: include non-HTML asset links in output (not fetched).

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -U pytest
.\.venv\Scripts\python.exe -m pytest -q
```
