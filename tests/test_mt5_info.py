import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.main import app

client = TestClient(app)

def test_get_mt5_info():
    response = client.get("/mt5-info")
    assert response.status_code == 200
    json_response = response.json()
    assert "login" in json_response
    assert "server" in json_response
    assert "status" in json_response
