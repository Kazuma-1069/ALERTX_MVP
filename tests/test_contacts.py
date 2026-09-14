from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_contact():
    response = client.post("/contacts", json={
        "name": "Sarah Jenkins",
        "phone": "+15552345678",
        "relationship": "Mom"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Sarah Jenkins"
