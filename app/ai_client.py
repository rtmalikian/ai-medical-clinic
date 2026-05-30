from __future__ import annotations

import httpx

from app.config import Settings, get_settings
from app.schemas import AIDraftRequest, AIDraftResponse


SYSTEM_PROMPT = """You are an administrative medical office workflow assistant. Draft only safe administrative text. Do not diagnose, treat, triage emergencies, or imply the message has been sent. Always keep human review required."""


class OpenAICompatibleClient:
    """Minimal OpenAI-compatible Chat Completions client.

    Works with providers that expose POST /chat/completions under an OpenAI-compatible base URL,
    including OpenAI, LiteLLM gateways, vLLM, local model servers, and many OpenRouter-style gateways.
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def is_configured(self) -> bool:
        return bool(self.settings.openai_api_key)

    def draft(self, request: AIDraftRequest) -> AIDraftResponse:
        if not self.is_configured():
            return fallback_draft(request)

        endpoint = self.settings.openai_base_url.rstrip("/") + "/chat/completions"
        user_prompt = (
            f"Workflow: {request.workflow_id}\n"
            f"Allowed task: {request.allowed_task}\n"
            f"Safety level: {request.safety_level}\n"
            f"Summary: {request.summary}\n\n"
            "Return concise text for staff review only."
        )
        payload = {
            "model": self.settings.openai_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 500,
        }
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}
        try:
            with httpx.Client(timeout=self.settings.request_timeout_seconds) as client:
                response = client.post(endpoint, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
            text = data["choices"][0]["message"]["content"].strip()
            return AIDraftResponse(
                provider="openai-compatible",
                model=self.settings.openai_model,
                draft_text=text,
                warnings=["Human review required before any patient communication or EHR action."],
            )
        except Exception:
            # Fail closed into deterministic fallback; do not leak provider errors/secrets to users.
            fallback = fallback_draft(request)
            fallback.warnings.append("AI provider call failed; safe deterministic fallback was used.")
            return fallback


def fallback_draft(request: AIDraftRequest) -> AIDraftResponse:
    text = (
        f"Draft for staff review ({request.workflow_id}): Review the case summary, verify patient identity, "
        f"check clinic policy, resolve missing information, and obtain human approval before any outbound message "
        f"or EHR action. Summary: {request.summary[:500]}"
    )
    return AIDraftResponse(
        provider="fallback",
        model=None,
        draft_text=text,
        warnings=["No AI API key configured; deterministic demo fallback used."],
    )
