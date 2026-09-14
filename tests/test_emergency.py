from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_start_and_complete():
    session = client.post("/emergency/start").json()
    sid = session["session_id"]
    assert session["status"] == "active"
    response = client.post(f"/emergency/{sid}/complete")
    assert response.json()["status"] == "completed"
