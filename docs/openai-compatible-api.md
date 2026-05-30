# OpenAI-Compatible AI Integration

The app can call external providers exposing the OpenAI Chat Completions API shape:

```text
POST {OPENAI_BASE_URL}/chat/completions
Authorization: use a server-side provider API key
```

It also exposes a local demo-compatible response shape:

```text
POST /v1/chat/completions
```

This local endpoint is intentionally not a raw paid-model proxy. It returns safe workflow-router text and directs real work to the workflow/review/audit APIs.

Runtime variables:

- `OPENAI_BASE_URL` or `AI_PROVIDER_BASE_URL`
- `OPENAI_API_KEY` or `AI_PROVIDER_API_KEY`
- `OPENAI_MODEL` or `AI_MODEL`
- `AI_REQUEST_TIMEOUT_SECONDS`

The app does not expose a raw unauthenticated LLM proxy. The public API endpoint `/api/ai/draft` accepts bounded workflow summaries and allowed task names, then returns a draft that still requires human approval.

## Guardrails

- Use server-side API keys only.
- Validate request body with Pydantic.
- Use small bounded prompts.
- Fail closed to deterministic fallback.
- Never send automatically.
- Never ask the model to diagnose or triage.
- Do not log provider secrets or raw PHI.
