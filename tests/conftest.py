import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("AI_MEDICAL_CLINIC_DEMO_MODE", "true")

@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)
