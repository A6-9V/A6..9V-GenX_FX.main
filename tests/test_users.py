import pytest
from fastapi.testclient import TestClient
import sys
import os
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.main import app
import sqlite3
from unittest.mock import patch

client = TestClient(app)

def test_get_users():
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        os.environ["DB_PATH"] = tmp.name
        conn = sqlite3.connect(tmp.name)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            is_active INTEGER NOT NULL
        )
        """)
        cursor.execute("INSERT INTO users VALUES (1, 'testuser', 'test@example.com', 1)")
        conn.commit()
        conn.close()

        response = client.get("/users")
        assert response.status_code == 200
        json_response = response.json()
        assert "users" in json_response
        assert len(json_response["users"]) > 0

        del os.environ["DB_PATH"]
