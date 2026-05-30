from __future__ import annotations

from collections import Counter
from typing import Any

import httpx

from app.schemas import FHIRBundleSummary


def normalize_bundle(bundle: dict[str, Any]) -> FHIRBundleSummary:
    entries = bundle.get("entry", []) if bundle.get("resourceType") == "Bundle" else []
    refs: list[str] = []
    counts: Counter[str] = Counter()
    for entry in entries:
        resource = entry.get("resource") or {}
        rtype = resource.get("resourceType")
        rid = resource.get("id")
        if not rtype:
            continue
        counts[rtype] += 1
        if rid:
            refs.append(f"{rtype}/{rid}")
    return FHIRBundleSummary(resource_count=sum(counts.values()), resource_refs=refs, resource_types=dict(counts))


async def fetch_capability_statement(base_url: str, bearer_token: str | None = None) -> dict[str, Any]:
    headers = {"Accept": "application/fhir+json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(base_url.rstrip("/") + "/metadata", headers=headers)
        response.raise_for_status()
        return response.json()
