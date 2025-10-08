# Project Instructions
>
> **Purpose**: Maintain and extend **openai-url-harvester**. Goals: enumerate and fetch all URLs on <https://platform.openai.com/docs/> and <https://cookbook.openai.com/>, enumerate and fetch all URLs disclosed in all_urls.txt, cookbook_urls.txt, and openai_best_practice_urls.txt, extract URLs from local files, and ship deterministic artifacts.
> **Tools**: Use `web_search`, `file_search`, and Code Interpreter when helpful. Choose tools yourself. Prefer hosted tools from the Responses API. ([OpenAI Platform][14])
> **Models and params**: Use **GPT-5**. Set reasoning effort = **minimal** for parsing and URL extraction, **medium** for code refactors, **high** for design docs. Keep verbosity low unless debugging. Use CFG when strict JSON or line-delimited URL output is required. ([OpenAI Cookbook][3])
> **Data sources**: Start from seeds in `seed_urls.txt` and the official indices: Cookbook index and key GPT-5 guides. Crawl only allow-listed hosts. ([OpenAI Cookbook][1])
> **Process**:
>
> 1. Crawl → dedupe → sort → write `cookbook_urls.txt`.
> 2. Fetch HTML to `/cache/` with stable filenames.
> 3. Extract URLs from local MD/HTML/JSON/TXT/PDF and write `all_urls.txt`.
> 4. Run evals: URL recall vs. last run, broken-link rate, diff summaries. ([OpenAI Cookbook][16])
> 5. Produce release bundle: URLs, inventory, and changelog; include provenance.
>    - **Safety**: Use end-user IDs; avoid non-allow-listed domains. ([OpenAI Platform][11])
>    - **Failure policy**: If uncertainty >20% or coverage gap detected, emit a remediation plan and request a targeted crawl.
>
[1]: https://cookbook.openai.com/?utm_source=chatgpt.com "OpenAI Cookbook"
[3]: https://cookbook.openai.com/examples/gpt-5/gpt-5_new_params_and_tools?utm_source=chatgpt.com "GPT-5 New Params and Tools"
[11]: https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids?utm_source=chatgpt.com "Safety best practices - OpenAI API"
[14]: https://platform.openai.com/docs/changelog/changelog?utm_source=chatgpt.com "Changelog - OpenAI API"
[16]: https://cookbook.openai.com/examples/evaluation/use-cases/web-search-evaluation?utm_source=chatgpt.com "Evals API Use-case - Web Search Evaluation"

## Global Performance Defaults (GPT-5 Thinking)

- **Model/effort**: Default GPT-5; choose minimal/medium/high reasoning per task complexity. Keep verbosity low unless debugging.
  <https://cookbook.openai.com/examples/gpt-5/gpt-5_new_params_and_tools?utm_source=chatgpt.com>

- **Prompting**: Apply the “six strategies” and Cookbook prompting patterns; pin output formats.
  <https://platform.openai.com/docs/guides/prompt-engineering/six-strategies-for-getting-better-results?utm_source=chatgpt.com>

- **Tooling**: Prefer Responses API hosted tools; log queries and sources.
  <https://platform.openai.com/docs/changelog/changelog?utm_source=chatgpt.com>

- **Accuracy**: Use the Optimizing LLM Accuracy guide to set RAG, evals, and guardrails.
  <https://platform.openai.com/docs/guides/optimizing-llm-accuracy/llm-optimization-context?utm_source=chatgpt.com>

- **Latency/cost**: Use Predicted Outputs when templates are known; cache aggressively.
  <https://platform.openai.com/docs/guides/predicted-outputs?utm_source=chatgpt.com>

- **Safety**: Follow end-user-ID and moderation guidance.
  <https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids?utm_source=chatgpt.com>
