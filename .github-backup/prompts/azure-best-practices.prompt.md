---
mode: agent
description: Run Azure best-practice prechecks and propose a plan
---
Task:
1) Call the appropriate best-practice tool:
   - general/code-generation or general/deployment
   - azurefunctions/code-generation or azurefunctions/deployment
2) Summarize recommendations as TODOs by risk and effort.
3) Ask for missing inputs.
4) Output a minimal, idempotent plan; request approval before edits.
