from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Health Check (already had this)
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# 2. Create Leave (Corrected)
def test_create_leave():
    payload = {"employee_id": "EMP01", "reason": "Sick", "days": 3}
    response = client.post("/leaves/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["employee_id"] == "EMP01"
    assert "id" in data
    # REMOVED: return data["id"]  <-- This was causing the warning

# 3. Test Getting All Leaves (New)
def test_get_leaves():
    # Create one first so the list isn't empty
    client.post("/leaves/", json={"employee_id": "EMP02", "reason": "Vacation", "days": 5})
    
    response = client.get("/leaves/")
    assert response.status_code == 200
    assert len(response.json()) > 0

# 4. Test Getting a Specific Leave (New)
def test_get_single_leave():
    # Create a leave
    setup_resp = client.post("/leaves/", json={"employee_id": "EMP03", "reason": "Test", "days": 1})
    leave_id = setup_resp.json()["id"]

    # Get it back
    response = client.get(f"/leaves/{leave_id}")
    assert response.status_code == 200
    assert response.json()["employee_id"] == "EMP03"

# 5. Test Getting a Non-Existent Leave (New - Covers 404 error)
def test_get_leave_not_found():
    response = client.get("/leaves/fake-id-123")
    assert response.status_code == 404
    assert response.json() == {"detail": "Leave not found"}

# 6. Test Deleting a Leave (New)
def test_delete_leave():
    # Create one
    setup_resp = client.post("/leaves/", json={"employee_id": "EMP04", "reason": "Delete Me", "days": 1})
    leave_id = setup_resp.json()["id"]

    # Delete it
    response = client.delete(f"/leaves/{leave_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}

    # Verify it is gone
    get_response = client.get(f"/leaves/{leave_id}")
    assert get_response.status_code == 404

# 7. Test Deleting a Non-Existent Leave (New - Covers Delete 404)
def test_delete_leave_not_found():
    response = client.delete("/leaves/fake-id-999")
    assert response.status_code == 404