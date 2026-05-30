from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings. Secrets are read from env only and never committed."""

    demo_mode: bool = os.getenv("AI_MEDICAL_CLINIC_DEMO_MODE", "true").lower() == "true"
    openai_base_url: str = os.getenv("OPENAI_BASE_URL") or os.getenv("AI_PROVIDER_BASE_URL", "https://api.openai.com/v1")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY") or os.getenv("AI_PROVIDER_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL") or os.getenv("AI_MODEL", "gpt-4o-mini")
    request_timeout_seconds: float = float(os.getenv("AI_REQUEST_TIMEOUT_SECONDS", "20"))


def get_settings() -> Settings:
    return Settings()
