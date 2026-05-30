def test_lists_all_skill_backed_workflows(client):
    response = client.get("/api/workflows")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 12
    ids = {item["id"] for item in data["workflows"]}
    assert "patient-intake-triage" in ids
    assert "prior-authorization" in ids
    assert "billing-denial-support" in ids


def test_workflow_run_blocks_missing_information(client):
    response = client.post("/api/workflows/patient-intake-triage/run", json={
        "source": "portal",
        "request_text": "Patient left a vague message",
        "use_ai": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "needs_information"
    assert "patient_identity" in data["missing_fields"]
    assert data["requires_human_approval"] is True
    assert data["safety_level"] == "review_required"


def test_workflow_run_escalates_urgent_content(client):
    response = client.post("/api/workflows/patient-message-drafting/run", json={
        "source": "portal",
        "patient_ref": "Patient/example",
        "request_text": "I have severe chest pain and shortness of breath, what should I do?",
        "use_ai": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "clinical_escalation"
    assert data["escalation_flags"]
    assert "No medical advice generated" in data["staff_checklist"]


def test_workflow_run_creates_review_task_and_audit_event(client):
    response = client.post("/api/workflows/appointment-scheduling/run", json={
        "source": "phone",
        "patient_ref": "Patient/example",
        "request_text": "I need a routine follow up visit next week in the afternoon.",
        "use_ai": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "routine_admin"
    assert data["review_task_id"]
    assert data["audit_event_id"]

    tasks = client.get("/api/review-tasks").json()["review_tasks"]
    assert any(task["id"] == data["review_task_id"] for task in tasks)
