---
mode: agent
description: Debug crawl issues and propose solutions
---

# Crawl Debugging Workflow

## Task
Diagnose and resolve crawl issues with the openai-url-harvester.

## Diagnostic Steps
1) **Check error logs**: Look for patterns in failed requests
2) **Validate robots.txt**: Ensure robots cache is working correctly
3) **Rate limiting analysis**: Check if QPS limits are being respected
4) **Content type filtering**: Verify only HTML/XHTML is being processed
5) **URL normalization**: Check for malformed or problematic URLs

## Common Issues
- **High error rates**: Usually robots.txt 5xx or rate limiting
- **Missing URLs**: Check allowlist domain matching
- **Slow crawls**: Verify aiolimiter configuration
- **Memory issues**: Check response size limits (60KB cap)

## Resolution Process
1) Identify root cause
2) Propose minimal fix preserving async patterns
3) Suggest test case to prevent regression
4) Wait for approval before implementing

## Commands for Diagnosis
```powershell
# Dry run for testing
.\.venv\Scripts\python.exe -m openai_url_harvester crawl --dry-run --start "https://example.com"

# Verbose logging
.\.venv\Scripts\python.exe -m openai_url_harvester crawl --verbose --max-pages 10
```