# Copilot Validation Checklist

## Discovery
- **Prompt files discovered**: type `/azure-best-practices` in Chat and confirm it loads.
- **Chat modes discovered**: open mode picker and verify **Harvester** and **Azure** appear.

## Mode Behavior
- **Switch to Harvester mode**: Verify tools listed in the picker are available and read-only actions are respected.
- **Switch to Azure mode**: Only when working in Azure repos or files; confirm tools are available.

## Instructions Precedence
- **Confirm workspace** `.github/copilot-instructions.md` applies in chat.
- **Confirm scoped** `.instructions.md` (the Azure rules file) only triggers on files matching `applyTo`.

## Agent Mode & Tools
- **Start Agent mode**: Approve tool use deliberately. Verify terminal/tool prompts appear with confirmation gates.

## Settings Spot-check
- **Settings: Prompt files** enabled and locations include `.github/prompts`.
- **Settings: Chat modes** locations include `.github/chatmodes`.
- **Settings: Instruction files** locations include `.github`.

## Notes
- Custom instructions affect chat, not inline completions.
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