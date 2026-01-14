from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test if the API is running"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_leave():
    """Test creating a new leave request"""
    payload = {"employee_id": "EMP01", "reason": "Sick", "days": 3}
    response = client.post("/leaves/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["employee_id"] == "EMP01"
    assert "id" in data