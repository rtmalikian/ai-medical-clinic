---
name: medical-records-requests
description: Use when mapping the medical records requests medical office workflow into atomic human steps, agentic automation opportunities, EHR/FHIR touchpoints, demo cases, and implementation acceptance criteria.
version: 1.0.0
author: Raphael T. Malikian, MBBS, BSc
license: Commercial Evaluation License
metadata:
  hermes:
    tags: [medical-office, healthcare-ai, clinic-automation, ehr, fhir, workflow]
    related_skills: []
---

# Medical Records Request Skill

## Overview

**Problem:** Release-of-information requests are document-heavy, deadline-sensitive, and risky if identity, authorization, or scope are wrong.

**Human owner today:** records / front desk / compliance contact.

**Target outcome:** ROI request classification, required-authorization checklist, deadline tracker, and packet preparation task.

This skill is designed for a no-PHI demo first, then a read-only EHR/FHIR pilot, then carefully governed human-approved production use. The agent should organize, summarize, draft, route, and remind. It should not make autonomous clinical decisions or send/write anything without approval.

## Current Human Workflow

1. Receive records request.
2. Identify requester and patient.
3. Determine request type and legal/authorization basis.
4. Verify signed authorization or permitted disclosure pathway.
5. Determine date range and document scope.
6. Collect responsive records.
7. Apply minimum necessary and clinic policy.
8. Prepare secure delivery method.
9. Log disclosure and provenance.
10. Close request and retain documentation.

## Atomic Step Breakdown

| # | Human atomic step | Agentic design note |
|---:|---|---|
| 1 | Receive records request. | draft/verify/route where safe; human review for final action |
| 2 | Identify requester and patient. | draft/verify/route where safe; human review for final action |
| 3 | Determine request type and legal/authorization basis. | draft/verify/route where safe; human review for final action |
| 4 | Verify signed authorization or permitted disclosure pathway. | draft/verify/route where safe; human review for final action |
| 5 | Determine date range and document scope. | draft/verify/route where safe; human review for final action |
| 6 | Collect responsive records. | draft/verify/route where safe; human review for final action |
| 7 | Apply minimum necessary and clinic policy. | draft/verify/route where safe; human review for final action |
| 8 | Prepare secure delivery method. | draft/verify/route where safe; human review for final action |
| 9 | Log disclosure and provenance. | draft/verify/route where safe; human review for final action |
| 10 | Close request and retain documentation. | draft/verify/route where safe; human review for final action |

## Agentic Replacement Map

### Steps the agent can assist or replace

- Classify request type.
- Extract requested date range/document types.
- Generate authorization checklist.
- Create deadline/reminder task.
- Draft requester response for missing authorization.
- Prepare document index.

### Steps that must remain human-reviewed

- Verify legal sufficiency.
- Approve disclosure.
- Handle sensitive records.
- Release records through approved channel.

### Recommended first automation boundary

Start with **draft-only mode**: the agent produces structured output, staff review/edit, and any outbound message or EHR update is completed by a human.

## Inputs

- Synthetic demo case data or de-identified workflow examples.
- Clinic-specific policy/SOP for this workflow.
- Patient request text, staff notes, portal messages, call transcript, form submission, fax metadata, or spreadsheet row.
- EHR/FHIR read-only resources when approved.
- Approved message templates and escalation rules.

## Outputs

- Structured case summary.
- Missing-information checklist.
- Recommended queue/category/status.
- Draft staff script or patient message.
- Human approval task.
- Audit event payload.
- Optional EHR writeback proposal, disabled by default.

## EHR / FHIR Touchpoints

Likely resources: **DocumentReference, Binary, Consent, Patient, Provenance, Task, Communication**.

Integration pattern:

1. Start with fixture JSON/CSV.
2. Add read-only FHIR resource fetches.
3. Normalize into a workflow `CaseFile` object.
4. Generate draft/checklist/task outputs.
5. Store proposed writeback as a pending human approval.
6. Only commit to EHR after customer-specific approval and audit logging.

Suggested SMART scopes should be least-privilege and workflow-specific. Avoid broad chart access when a task only needs appointment, coverage, or communication metadata.

## Safety and Human Review

- Demo data must be synthetic or properly de-identified.
- Do not use for emergencies, diagnosis, treatment, or autonomous clinical triage.
- Do not send patient communications automatically.
- Do not write to the EHR automatically.
- Route clinical uncertainty, urgent symptoms, abnormal results, medication changes, and patient safety concerns to authorized staff.
- Keep audit logs of source references, generated draft, reviewer, final action, and timestamp.

## Demo Test Cases

### Case 1: Clean routine request

Input: a complete synthetic request with all required fields.

Expected output:

- correct workflow category;
- concise summary;
- no missing critical fields;
- safe draft response;
- low escalation risk.

### Case 2: Missing information

Input: a realistic but incomplete request.

Expected output:

- missing-information checklist;
- draft follow-up questions;
- no final action recommendation until missing data is resolved.

### Case 3: Clinical or safety escalation

Input: a request containing symptoms, abnormal result concern, medication issue, urgent phrasing, or ambiguity.

Expected output:

- escalation flag;
- no medical advice;
- staff-routing recommendation;
- safe acknowledgement draft only if clinic policy allows.

## Implementation Checklist

- [ ] Write fixture data for the three demo cases.
- [ ] Define Zod/Pydantic schema for input and output.
- [ ] Implement deterministic classifier/rules before LLM drafting.
- [ ] Add LLM draft generation behind server-side API only.
- [ ] Validate structured model output against schema.
- [ ] Add urgent/clinical content guardrail.
- [ ] Add human approval state machine: draft → reviewed → approved/rejected → final action.
- [ ] Add audit event for every generated draft and human action.
- [ ] Add FHIR adapter with read-only fixture mode.
- [ ] Add tests for clean, missing-info, and escalation cases.

## Metrics

- Staff minutes saved per case.
- Queue aging reduction.
- Fewer missed follow-ups.
- Faster patient response time.
- Fewer incomplete tasks returned to staff.
- Human acceptance/edit rate of agent drafts.

## Common Pitfalls

1. **Over-automating too early.** Draft-only mode is easier to sell and safer to validate.
2. **Ignoring clinic policy.** The agent must use clinic-specific templates, not generic healthcare advice.
3. **Treating EHR writeback as required.** Most pilots can prove value before writeback.
4. **Letting PHI leak into logs or prompts.** Minimize, redact, and avoid public demos with real data.
5. **Failing to separate admin from clinical content.** Clinical uncertainty should route to qualified staff.

## Verification Checklist

- [ ] The workflow can be demoed with no PHI.
- [ ] Every output is traceable to an input/source reference.
- [ ] Patient-facing language is reviewed by a human.
- [ ] Clinical-risk cases fail closed into escalation.
- [ ] EHR integration is read-only unless explicitly approved.
- [ ] Metrics are measurable before and after pilot.
