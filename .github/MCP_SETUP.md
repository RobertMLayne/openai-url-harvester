# MCP Servers Configuration

This workspace uses Model Context Protocol (MCP) servers to extend Copilot's capabilities with specialized tools for web crawling and project management.

## Configured Servers

### Core Development Servers

- **GitHub**: Remote API access for issues, PRs, and repository operations
- **Git**: Local Git operations (staging, commits, diffs)
- **Filesystem**: Scoped file I/O within the workspace
- **SQLite**: Results store for crawled URL inventory in `.cache/harvest.db`

### Web Crawling Servers

- **Fetch**: Fast HTML fetch and text conversion for static pages
- **Playwright**: Browser automation for JS-rendered pages and screenshots
- **Brave Search**: High-quality web search results

### Optional Servers

- **OpenAPI**: Convert API specifications into tools (when specs are added to `openapi/` directory)

## Setup Instructions

1. **Install required tools**: Ensure `uvx` and `npx` are available in your PATH
2. **Brave Search API**: Get an API key from [Brave Search API](https://brave.com/search/api/) and set the `BRAVE_API_KEY` environment variable
3. **Reload VS Code**: After configuration changes, reload the window for MCP servers to initialize

## Usage Examples

### Web Crawling Workflow
```
1. Use Fetch server to retrieve static HTML content
2. Use Playwright for JavaScript-heavy sites requiring browser rendering
3. Store results in SQLite database via the SQLite server
4. Use Git server to commit crawl results and configurations
```

### Development Workflow
```
1. Use Filesystem server for safe workspace file operations
2. Use GitHub server for issue/PR management
3. Use Git server for version control operations
4. Use Brave Search for research and documentation lookup
```

## Security Notes

- All servers are workspace-scoped except GitHub (which uses Copilot's authenticated session)
- Filesystem access is restricted to the workspace root
- SQLite database is isolated to `.cache/harvest.db`
- API keys should be set as environment variables, not hardcoded

## Troubleshooting

If MCP servers fail to load:
1. Check that `uvx` is installed: `pip install uv`
2. Verify `npx` is available: `npm --version`
3. Check VS Code Developer Tools Console for MCP errors
4. Ensure environment variables are set correctly

## Tool Limits

VS Code Copilot Agent Mode has a 128-tool limit. This configuration uses 8 core servers, leaving room for additional tools as needed.