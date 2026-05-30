from __future__ import annotations

import hashlib
import json
from typing import Any

from app.schemas import AuditEvent

AUDIT_EVENTS: list[AuditEvent] = []


def stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def record_event(event: AuditEvent) -> AuditEvent:
    AUDIT_EVENTS.append(event)
    return event


def list_events() -> list[AuditEvent]:
    return list(AUDIT_EVENTS)
