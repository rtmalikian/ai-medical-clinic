from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

SourceType = Literal["call", "phone", "portal", "fax", "form", "csv", "fhir", "email", "web"]
SafetyLevel = Literal["demo_only", "review_required", "clinical_escalation"]
ReviewStatus = Literal["pending", "approved", "rejected", "changes_requested"]


class WorkflowCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: SourceType = "form"
    patient_ref: str | None = None
    request_text: str | None = Field(default=None, max_length=12_000)
    data: dict[str, Any] = Field(default_factory=dict)
    fhir_refs: list[str] = Field(default_factory=list)
    clinic_policy_refs: list[str] = Field(default_factory=list)
    use_ai: bool = False


class WorkflowSummary(BaseModel):
    id: str
    title: str
    block: str
    description: str
    fhir_touchpoints: list[str]
    skill_path: str


class WorkflowRunOutput(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid4()))
    workflow_id: str
    summary: str
    category: str
    missing_fields: list[str] = Field(default_factory=list)
    escalation_flags: list[str] = Field(default_factory=list)
    draft_message: str | None = None
    staff_checklist: list[str] = Field(default_factory=list)
    proposed_tasks: list[str] = Field(default_factory=list)
    safety_level: SafetyLevel = "review_required"
    requires_human_approval: bool = True
    review_task_id: str | None = None
    audit_event_id: str | None = None


class AIDraftRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: str
    summary: str = Field(max_length=8_000)
    allowed_task: Literal["draft_patient_message", "draft_internal_checklist", "summarize_case", "draft_staff_script"]
    safety_level: SafetyLevel = "review_required"


class AIDraftResponse(BaseModel):
    provider: str
    model: str | None = None
    draft_text: str
    requires_human_approval: bool = True
    warnings: list[str] = Field(default_factory=list)


class ReviewTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    workflow_id: str
    run_id: str
    status: ReviewStatus = "pending"
    title: str
    artifact: WorkflowRunOutput
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewer_note: str | None = None


class AuditEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor_type: Literal["system", "human", "llm", "external_service"] = "system"
    action: str
    workflow_id: str | None = None
    run_id: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    artifact_hash: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class FHIRBundleSummary(BaseModel):
    resource_count: int
    resource_refs: list[str]
    resource_types: dict[str, int]


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="allow")

    role: Literal["system", "user", "assistant", "tool"]
    content: str | None = None


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = "ai-medical-clinic-workflow-router"
    messages: list[ChatMessage]
    temperature: float | None = None
    stream: bool = False
