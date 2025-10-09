# Copilot Validation Checklist

## Discovery

- **Prompt files discovered**: type `/azure-best-practices`, `/crawl-quality-report`, `/crawl-debug` in Chat and confirm they load.
- **Chat modes discovered**: open mode picker and verify **Harvester**, **ReleaseManager**, and **Azure** appear.
- **Collections available**: confirm `crawler-ops` collection is discoverable.

## Mode Behavior

- **Switch to Harvester mode**: Verify tools listed for crawler maintenance and read-only operations.
- **Switch to ReleaseManager mode**: Confirm deployment-focused tools and terminal access.
- **Switch to Azure mode**: Only when working in Azure repos or files; confirm Azure tools are available.

## Instructions Precedence

- **Confirm workspace** `.github/copilot-instructions.md` applies in chat.
- **Confirm scoped** `.instructions.md` files only trigger on files matching `applyTo`.
- **Python files**: Should get openai-url-harvester specific guidance.
- **Azure files** (.bicep, .tf): Should get Azure rules + harvester guidance.

## Agent Mode & Tools

- **Start Agent mode**: Approve tool use deliberately. Verify terminal/tool prompts appear with confirmation gates.
- **Collections**: Test loading the `crawler-ops` collection bundle.

## Settings Spot-check

- **Settings: Prompt files** enabled and locations include `.github/prompts`.
- **Settings: Chat modes** locations include `.github/chatmodes`.
- **Settings: Instruction files** locations include `.github/instructions` and `.github`.
- **Settings: Collections** locations include `.github/collections`.

## Workflow Validation

### Crawler Development Workflow

1. **Open Python file** → Gets harvester instructions automatically
2. **Switch to Harvester mode** → Specialized crawler maintenance persona
3. **Use `/crawl-debug`** → Troubleshooting workflow
4. **Use `/crawl-quality-report`** → Analysis and reporting

### Release Workflow

1. **Switch to ReleaseManager mode** → Deployment-focused tools
2. **Run quality gates** → Automated validation
3. **Generate artifacts** → Sitemap, CSV, URL lists

### Azure Workflow

1. **Open .bicep/.tf file** → Gets Azure rules + harvester context
2. **Switch to Azure mode** → Cross-workspace Azure helper
3. **Use `/azure-best-practices`** → Structured Azure workflow

## Notes

- Custom instructions affect chat, not inline completions.
- Keep secrets and tokens out of prompts and instruction files.
- Collections provide bundled workflows for common tasks.
- Scoped instructions maintain separation between Azure and crawler concerns.
- Keep secrets and tokens out of prompts and instruction files.

## Expected Behavior

### Workspace Chat (any file)

- Uses `.github/copilot-instructions.md` for openai-url-harvester guidance
- Rate limiting, robots.txt compliance, PowerShell examples

### Azure Files (.bicep, .tf, workflows)

- Inherits workspace instructions + adds Azure rules
- Calls best-practices tools before code generation
- Plans before edits

### Prompt Usage

- `/azure-best-practices` → Agent mode Azure workflow
- Works in any workspace context

### Chat Modes

- **Harvester**: Project-focused with read-only tools
- **Azure**: Cross-workspace Azure development helper
