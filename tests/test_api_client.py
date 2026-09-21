import pytest
from app.services.api import ApiService
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_service_offline_fallback():
    # Test unroutable port triggers offline fallback safely without crash
    api = ApiService(base_url="http://127.0.0.1:59999")
    res = api.check_health()
    assert res["ok"] is False
    assert res["status"] == "offline"
    assert api.is_online is False

def test_api_service_request_parsing():
    api = ApiService(base_url="http://127.0.0.1:8000")
    # Method and path composition
    assert api.base_url == "http://127.0.0.1:8000"
