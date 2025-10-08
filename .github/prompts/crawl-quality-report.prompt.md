---
mode: agent
description: Analyze crawl results and generate quality report
---

# Crawl Quality Analysis

## Task
Analyze the latest crawl results and generate a comprehensive quality report.

## Steps
1) **Load crawl artifacts**: Examine CSV details, URL lists, and any error logs
2) **Compare with baseline**: Check URL count vs previous runs, identify new/missing URLs
3) **Validate politeness**: Confirm rate limiting was respected (check timestamps in CSV)
4) **Check robots compliance**: Verify no disallowed URLs were crawled
5) **Generate report**: Summarize findings with recommendations

## Output Format
```markdown
# Crawl Quality Report - [Date]

## Summary
- Total URLs: [count]
- New URLs: [count]
- Errors: [count]
- Robots compliance: [✅/❌]

## Findings
[Key observations]

## Recommendations
[Action items by priority]
```

Request approval before running any validation commands.