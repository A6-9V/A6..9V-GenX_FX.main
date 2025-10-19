import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.main import app

client = TestClient(app)

def test_get_predictions():
    response = client.get("/api/v1/predictions")
    assert response.status_code == 200
    json_response = response.json()
    assert "predictions" in json_response
    assert "status" in json_response
    assert "timestamp" in json_response
