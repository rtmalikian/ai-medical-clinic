from __future__ import annotations

from typing import Any
from time import time
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query

from app.ai_client import OpenAICompatibleClient
from app.audit import list_events, record_event
from app.fhir.client import fetch_capability_statement, normalize_bundle
from app.review import list_review_tasks, update_review_task
from app.schemas import AIDraftRequest, AuditEvent, ChatCompletionRequest, WorkflowCase
from app.engine import run_workflow
from app.workflow_registry import get_workflow, list_workflows

app = FastAPI(
    title="AI Medical Clinic",
    description="Modular, human-in-the-loop medical office AI workflow automation with FHIR/EHR and OpenAI-compatible integration.",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "name": "AI Medical Clinic",
        "description": "Agentic medical office workflow automation demo with human review, audit logs, FHIR utilities, and OpenAI-compatible AI drafting.",
        "docs": "/docs",
        "safety": "Demo only. Do not enter PHI. Human approval required.",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/workflows")
def workflows() -> dict[str, Any]:
    items = list_workflows()
    return {"count": len(items), "workflows": [item.model_dump() for item in items]}


@app.get("/api/workflows/{workflow_id}")
def workflow_detail(workflow_id: str) -> dict[str, Any]:
    workflow = get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Unknown workflow")
    return workflow.model_dump()


@app.post("/api/workflows/{workflow_id}/run")
def run_workflow_endpoint(workflow_id: str, case: WorkflowCase) -> dict[str, Any]:
    try:
        output = run_workflow(workflow_id, case)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown workflow")
    return output.model_dump(mode="json")


@app.post("/api/ai/draft")
def ai_draft(request: AIDraftRequest) -> dict[str, Any]:
    workflow = get_workflow(request.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Unknown workflow")
    response = OpenAICompatibleClient().draft(request)
    record_event(AuditEvent(
        actor_type="llm" if response.provider != "fallback" else "system",
        action="ai_draft_generated",
        workflow_id=request.workflow_id,
        metadata={"provider": response.provider, "model": response.model, "human_review_required": True},
    ))
    return response.model_dump(mode="json")


@app.get("/api/review-tasks")
def review_tasks() -> dict[str, Any]:
    return {"review_tasks": [task.model_dump(mode="json") for task in list_review_tasks()]}


@app.post("/api/review-tasks/{task_id}/approve")
def approve_task(task_id: str, note: str | None = None) -> dict[str, Any]:
    task = update_review_task(task_id, "approved", note)
    if not task:
        raise HTTPException(status_code=404, detail="Unknown review task")
    record_event(AuditEvent(action="review_task_approved", workflow_id=task.workflow_id, run_id=task.run_id, resource_type="ReviewTask", resource_id=task.id))
    return task.model_dump(mode="json")


@app.post("/api/review-tasks/{task_id}/reject")
def reject_task(task_id: str, note: str | None = None) -> dict[str, Any]:
    task = update_review_task(task_id, "rejected", note)
    if not task:
        raise HTTPException(status_code=404, detail="Unknown review task")
    record_event(AuditEvent(action="review_task_rejected", workflow_id=task.workflow_id, run_id=task.run_id, resource_type="ReviewTask", resource_id=task.id))
    return task.model_dump(mode="json")


@app.get("/api/audit-events")
def audit_events() -> dict[str, Any]:
    return {"audit_events": [event.model_dump(mode="json") for event in list_events()]}


@app.post("/v1/chat/completions")
def local_openai_compatible_chat(request: ChatCompletionRequest) -> dict[str, Any]:
    """Local OpenAI-compatible response shape for demos and agent integrations.

    This is intentionally not a raw LLM proxy. It returns a safe clinic-workflow assistant
    response and keeps all real actions behind the workflow/review APIs.
    """
    if request.stream:
        raise HTTPException(status_code=400, detail="Streaming is not supported in the local demo endpoint")
    user_text = "\n".join((m.content or "") for m in request.messages if m.role == "user")[-1200:]
    content = (
        "AI Medical Clinic workflow assistant draft (human review required): "
        "Use the workflow APIs to run deterministic checks, create a review task, and record an audit event. "
        f"Received request summary: {user_text}"
    )
    return {
        "id": f"chatcmpl-{uuid4().hex}",
        "object": "chat.completion",
        "created": int(time()),
        "model": request.model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


@app.post("/api/fhir/normalize-bundle")
def normalize_fhir_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return normalize_bundle(bundle).model_dump()


@app.get("/api/fhir/capability")
async def fhir_capability(base_url: str = Query(..., description="FHIR base URL, e.g. https://hapi.fhir.org/baseR4")) -> dict[str, Any]:
    try:
        statement = await fetch_capability_statement(base_url)
    except Exception:
        raise HTTPException(status_code=502, detail="Could not fetch FHIR CapabilityStatement")
    return {
        "resourceType": statement.get("resourceType"),
        "fhirVersion": statement.get("fhirVersion"),
        "software": statement.get("software", {}),
        "rest_count": len(statement.get("rest", [])),
    }
