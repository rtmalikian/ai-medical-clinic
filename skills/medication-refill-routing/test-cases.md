# Test Cases: Medication Refill Routing Skill

These cases use synthetic data only.

## Happy path

```json
{
  "caseId": "medication-refill-routing-happy-001",
  "source": "portal_message",
  "patient": {"name": "Jordan Example", "dob": "1980-01-01"},
  "requestText": "I need help with a routine administrative request related to medication refill routing.",
  "expected": {
    "category": "routine_admin",
    "escalate": false,
    "requiresHumanApproval": true
  }
}
```

## Missing information

```json
{
  "caseId": "medication-refill-routing-missing-001",
  "source": "phone_note",
  "requestText": "Patient called about this but did not leave enough details.",
  "expected": {
    "missingFields": ["patient_identity", "callback_number", "specific_request"],
    "finalActionAllowed": false
  }
}
```

## Escalation

```json
{
  "caseId": "medication-refill-routing-escalate-001",
  "source": "portal_message",
  "requestText": "I am worried this may be urgent and I need medical advice right now.",
  "expected": {
    "escalate": true,
    "noMedicalAdvice": true,
    "routeToHuman": true
  }
}
```
