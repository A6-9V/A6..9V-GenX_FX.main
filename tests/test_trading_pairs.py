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

def test_get_trading_pairs():
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        os.environ["DB_PATH"] = tmp.name
        conn = sqlite3.connect(tmp.name)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE trading_pairs (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            base_currency TEXT NOT NULL,
            quote_currency TEXT NOT NULL,
            is_active INTEGER NOT NULL
        )
        """)
        cursor.execute("INSERT INTO trading_pairs VALUES (1, 'EURUSD', 'EUR', 'USD', 1)")
        conn.commit()
        conn.close()

        response = client.get("/trading-pairs")
        assert response.status_code == 200
        json_response = response.json()
        assert "trading_pairs" in json_response
        assert len(json_response["trading_pairs"]) > 0

        del os.environ["DB_PATH"]
