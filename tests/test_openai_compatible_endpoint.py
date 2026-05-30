def test_local_openai_compatible_chat_completions_endpoint(client):
    response = client.post("/v1/chat/completions", json={
        "model": "ai-medical-clinic-workflow-router",
        "messages": [
            {"role": "system", "content": "You are helping clinic staff."},
            {"role": "user", "content": "Create a safe draft for referral tracking."}
        ],
        "stream": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "chat.completion"
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert "human review" in data["choices"][0]["message"]["content"].lower()
