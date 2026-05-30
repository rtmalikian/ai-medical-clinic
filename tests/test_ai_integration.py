def test_ai_draft_endpoint_uses_safe_fallback_without_api_key(client, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AI_PROVIDER_API_KEY", raising=False)
    response = client.post("/api/ai/draft", json={
        "workflow_id": "referral-tracking",
        "summary": "Synthetic referral needs missing records follow-up.",
        "allowed_task": "draft_internal_checklist",
        "safety_level": "review_required"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "fallback"
    assert data["requires_human_approval"] is True
    assert "review" in data["draft_text"].lower()
