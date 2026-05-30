# Implementation Notes: Lab and Imaging Follow-Up Skill

## Minimal no-PHI implementation

1. Create fixture schema for `lab-imaging-follow-up` cases.
2. Build deterministic parser/classifier for obvious fields.
3. Add LLM drafting only after deterministic guardrails.
4. Render output in a human approval queue.
5. Store audit event with source ids and draft hash.

## Suggested data contract

```ts
export type WorkflowCase = {
  caseId: string;
  workflow: "lab-imaging-follow-up";
  source: "call" | "portal" | "fax" | "form" | "csv" | "fhir";
  requestText?: string;
  patientRef?: string;
  fhirRefs?: string[];
  clinicPolicyRefs?: string[];
};

export type WorkflowOutput = {
  summary: string;
  category: string;
  missingFields: string[];
  escalationFlags: string[];
  draftMessage?: string;
  staffChecklist: string[];
  proposedTasks: string[];
  requiresHumanApproval: true;
};
```

## Acceptance tests

- Happy path produces complete summary and safe draft.
- Missing-info case asks questions and blocks final action.
- Escalation case refuses medical advice and routes to staff.
- Output validates against schema.
- Audit event is created for draft generation.
- EHR writeback remains disabled by default.
