def test_fhir_bundle_normalization_extracts_resource_refs(client):
    bundle = {
        "resourceType": "Bundle",
        "entry": [
            {"resource": {"resourceType": "Patient", "id": "p1"}},
            {"resource": {"resourceType": "Appointment", "id": "a1"}}
        ]
    }
    response = client.post("/api/fhir/normalize-bundle", json=bundle)
    assert response.status_code == 200
    data = response.json()
    assert data["resource_count"] == 2
    assert "Patient/p1" in data["resource_refs"]
    assert "Appointment/a1" in data["resource_refs"]
