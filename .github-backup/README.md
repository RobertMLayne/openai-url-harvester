# Copilot Configuration

This directory contains a comprehensive Copilot setup following [awesome-copilot](https://github.com/github/awesome-copilot) patterns.

## Structure

```
.github/
├── copilot-instructions.md          # Global workspace instructions
├── instructions/                    # Scoped instruction files
│   ├── openai-url-harvester.instructions.md  # Python/crawler rules
│   └── azure.rules.instructions.md  # Azure-specific rules
├── prompts/                         # On-demand workflows
│   ├── azure-best-practices.prompt.md
│   ├── crawl-quality-report.prompt.md
│   └── crawl-debug.prompt.md
├── chatmodes/                       # Specialized personas
│   ├── Harvester.chatmode.md        # Crawler maintenance
│   ├── ReleaseManager.chatmode.md   # Deployment & QA
│   └── Azure.chatmode.md            # Azure development
├── collections/                     # Bundled workflows
│   └── crawler.collection.yml       # Complete crawler ops
└── COPILOT_VALIDATION.md            # Testing checklist
```

## Usage Patterns

### Auto-Applied Instructions

- **Any Python file**: Gets crawler-specific guidance automatically
- **Azure files** (.bicep, .tf, workflows): Gets Azure rules + crawler context
- **All files**: Gets global workspace instructions

### On-Demand Prompts

- `/azure-best-practices` → Structured Azure development workflow
- `/crawl-quality-report` → Analyze crawl results and generate reports
- `/crawl-debug` → Troubleshoot crawl issues with guided diagnostics

### Chat Mode Personas

- **Harvester**: Crawler maintenance and optimization
- **ReleaseManager**: Deployment, quality gates, artifact generation
- **Azure**: Cross-workspace Azure development helper

### Collection Bundles

- `crawler-ops`: Complete workflow bundle for all crawler operations

## Quality Gates

- **File naming**: Follow `*.instructions.md`, `*.prompt.md`, `*.chatmode.md` patterns
- **Frontmatter**: Use `applyTo:` for scoping, `tools:` for mode configuration
- **Validation**: Run checklist in `COPILOT_VALIDATION.md` before releases
- **Separation**: Keep Azure and crawler concerns isolated via scoping

## Team Workflow

1. **Development**: Switch to Harvester mode for code changes
2. **Quality**: Use `/crawl-quality-report` for analysis
3. **Debugging**: Use `/crawl-debug` for troubleshooting
4. **Release**: Switch to ReleaseManager mode for deployments
5. **Infrastructure**: Use Azure mode for infrastructure changes

All configuration is workspace-scoped and won't affect other projects.
