# Implementation Plan

## Phase 1: Demo API

- List all workflow modules.
- Run deterministic missing-info and escalation checks.
- Create review task for every workflow output.
- Record audit event for every workflow run.
- Add OpenAI-compatible fallback and optional provider call.
- Add FHIR Bundle normalization.

## Phase 2: Real persistence

Replace in-memory stores with Postgres tables:

- workflow_runs
- review_tasks
- audit_events
- ai_draft_runs
- fhir_resources

## Phase 3: EHR sandbox

Add SMART launch and read-only FHIR client.

## Phase 4: Human-approved writeback

Add pending writeback objects, approval diff, idempotency keys, and vendor-specific FHIR POST support.

## Phase 5: Clinic pilot package

Add setup wizard, workflow discovery intake form, reporting dashboard, and one polished pilot flow.
