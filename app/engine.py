from __future__ import annotations

import re

from app.ai_client import OpenAICompatibleClient
from app.audit import record_event, stable_hash
from app.review import create_review_task
from app.schemas import AIDraftRequest, AuditEvent, WorkflowCase, WorkflowRunOutput
from app.workflow_registry import get_workflow

URGENT_PATTERNS = re.compile(
    r"\b(chest pain|shortness of breath|can'?t breathe|stroke|suicidal|severe bleeding|emergency|urgent medical advice|right now)\b",
    re.IGNORECASE,
)


def _patient_identity_present(case: WorkflowCase) -> bool:
    if case.patient_ref:
        return True
    keys = {k.lower() for k in case.data.keys()}
    return bool({"patient_name", "name", "dob", "mrn", "patient_id"} & keys)


def run_workflow(workflow_id: str, case: WorkflowCase) -> WorkflowRunOutput:
    workflow = get_workflow(workflow_id)
    if not workflow:
        raise KeyError(workflow_id)

    text = case.request_text or ""
    missing: list[str] = []
    escalation_flags: list[str] = []
    staff_checklist = [
        "Verify patient identity and clinic authorization.",
        "Review generated output before patient communication or EHR action.",
        "Document human approval in the audit trail.",
    ]

    if not _patient_identity_present(case):
        missing.append("patient_identity")
    if not text.strip() and not case.data:
        missing.append("request_text_or_structured_data")

    if URGENT_PATTERNS.search(text):
        escalation_flags.append("Potential urgent or clinical-risk content detected")
        category = "clinical_escalation"
        safety_level = "clinical_escalation"
        staff_checklist.insert(0, "No medical advice generated")
        draft_message = "This message may involve urgent or clinical concerns. Route to qualified clinic staff immediately according to clinic policy. Do not use AI-generated medical advice."
        proposed_tasks = ["Escalate to licensed staff", "Record routing decision", "Follow clinic emergency/urgent-message SOP"]
    elif missing:
        category = "needs_information"
        safety_level = "review_required"
        draft_message = f"Please collect missing information before proceeding: {', '.join(missing)}. Human review is required."
        proposed_tasks = ["Request missing information", "Keep workflow in pending status"]
    else:
        category = "routine_admin"
        safety_level = "review_required"
        draft_message = f"Administrative draft for {workflow.title}: summarize request, verify policy, and prepare next-step task for staff review."
        proposed_tasks = ["Review administrative draft", "Approve or edit response", "Complete action in source system"]

    output = WorkflowRunOutput(
        workflow_id=workflow_id,
        summary=f"{workflow.title}: {text[:300] if text else 'Structured data case'}",
        category=category,
        missing_fields=missing,
        escalation_flags=escalation_flags,
        draft_message=draft_message,
        staff_checklist=staff_checklist,
        proposed_tasks=proposed_tasks,
        safety_level=safety_level,  # type: ignore[arg-type]
    )

    if case.use_ai and category == "routine_admin":
        ai_response = OpenAICompatibleClient().draft(AIDraftRequest(
            workflow_id=workflow_id,
            summary=output.summary,
            allowed_task="draft_internal_checklist",
            safety_level=output.safety_level,
        ))
        output.draft_message = ai_response.draft_text

    task = create_review_task(workflow_id, output)
    output.review_task_id = task.id

    event = record_event(AuditEvent(
        action="workflow_run_created",
        workflow_id=workflow_id,
        run_id=output.run_id,
        resource_type="WorkflowRunOutput",
        resource_id=output.run_id,
        artifact_hash=stable_hash(output.model_dump(mode="json")),
        metadata={"category": category, "safety_level": safety_level, "review_task_id": task.id},
    ))
    output.audit_event_id = event.id
    # Keep review artifact aligned with final IDs.
    task.artifact = output
    return output
