# AI Medical Clinic Architecture

The application uses a rules-first, AI-second, human-final architecture.

```text
Workflow request
  -> Pydantic validation
  -> deterministic safety/missing-info rules
  -> optional OpenAI-compatible draft generation
  -> review task
  -> audit event
  -> human approval/rejection
```

## Why this architecture

Medical office automation is sensitive because administrative work can still affect patient access, billing, privacy, and clinical routing. Therefore, the LLM never owns the workflow state. The LLM only drafts text after deterministic checks allow it.

## Core components

- `app/workflow_registry.py` lists 12 skill-backed modules.
- `app/engine.py` runs deterministic rules and creates review tasks.
- `app/ai_client.py` calls OpenAI-compatible `/chat/completions` endpoints or safe fallback.
- `app/review.py` stores human approval tasks for the demo.
- `app/audit.py` records append-only audit events.
- `app/fhir/client.py` provides FHIR Bundle and CapabilityStatement utilities.
