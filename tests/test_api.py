import pytest
import asyncio
from unittest.mock import Mock, patch
import os

# Skip tests if FastAPI is not available
try:
    from fastapi.testclient import TestClient
    from api.main import app, get_db
    from unittest.mock import MagicMock, PropertyMock
    import sqlite3
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

if FASTAPI_AVAILABLE:
    # Set test environment variables
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
    os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test"
    os.environ["REDIS_URL"] = "redis://localhost:6379"
    
    client = TestClient(app)
else:
    client = None

@pytest.fixture
def mock_auth():
    """Mock authentication"""
    with patch('api.utils.auth.get_current_user') as mock_user:
        mock_user.return_value = {"username": "testuser"}
        yield mock_user

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

@pytest.mark.asyncio
async def test_ml_service():
    """Test ML service"""
    from api.services.ml_service import MLService
    
    service = MLService()
    await service.initialize()
    
    # Test prediction
    prediction = await service.predict("BTCUSDT", {})
    assert "signal" in prediction
    assert "confidence" in prediction
    
    # Test health check
    health = await service.health_check()
    assert health == "healthy"
    
    await service.shutdown()

@pytest.mark.asyncio
async def test_data_service():
    """Test data service"""
    from api.services.data_service import DataService
    
    service = DataService()
    await service.initialize()
    
    # Test get data
    data = await service.get_realtime_data("BTCUSDT")
    assert data is not None
    
    # Test health check
    health = await service.health_check()
    assert health == "healthy"
    
    await service.shutdown()

def test_technical_indicators():
    """Test technical indicators"""
    import pandas as pd
    from core.indicators import TechnicalIndicators
    
    # Create sample data
    data = pd.DataFrame({
        'open': [100, 101, 102, 103, 104],
        'high': [105, 106, 107, 108, 109],
        'low': [95, 96, 97, 98, 99],
        'close': [102, 103, 104, 105, 106],
        'volume': [1000, 1100, 1200, 1300, 1400]
    })
    
    indicators = TechnicalIndicators()
    result = indicators.add_all_indicators(data)
    
    # Check that indicators were added
    assert 'rsi' in result.columns
    assert 'macd' in result.columns
    assert 'sma_20' in result.columns

def test_pattern_detector():
    """Test pattern detector"""
    import pandas as pd
    from core.patterns import PatternDetector
    
    # Create sample data
    data = pd.DataFrame({
        'open': [100, 102, 101, 103, 102],
        'high': [105, 106, 107, 108, 109],
        'low': [95, 96, 97, 98, 99],
        'close': [102, 101, 105, 104, 107],
        'volume': [1000, 1100, 1200, 1300, 1400]
    })
    
    detector = PatternDetector()
    patterns = detector.detect_patterns(data)
    
    # Check that patterns were detected
    assert 'bullish_engulfing' in patterns
    assert 'bearish_engulfing' in patterns
    assert 'doji' in patterns

def test_config_loading():
    """Test config loading"""
    from utils.config import load_config
    
    config = load_config("non_existent_file.json")
    assert isinstance(config, dict)
    assert "database_url" in config
    assert "symbols" in config

def test_paginated_users_endpoint():
    """
    Tests the /users/paginated endpoint for correct pagination and response structure.
    """
    # --- Mock database dependency ---
    mock_db = MagicMock()
    mock_cursor = MagicMock()

    # Simulate 20 users in the database
    mock_users = []
    for i in range(20):
        mock_user = MagicMock(spec=sqlite3.Row)
        mock_user.keys.return_value = ["username", "email", "is_active"]
        mock_user.__getitem__.side_effect = {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "is_active": 1
        }.__getitem__
        mock_users.append(mock_user)

    def mock_execute(query, params=None):
        if "LIMIT" in query:
            limit, offset = params
            mock_cursor.fetchall.return_value = mock_users[offset : offset + limit]
        elif "COUNT" in query:
            mock_cursor.fetchone.return_value = (20,)

    mock_cursor.execute.side_effect = mock_execute
    mock_db.cursor.return_value = mock_cursor

    def override_get_db():
        try:
            yield mock_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # --- Test with limit and offset ---
    response = client.get("/users/paginated?offset=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 5
    assert data["users"][0]["username"] == "user5"
    assert data["total"] == 20

    # --- Test with default parameters (limit=10, offset=0) ---
    response = client.get("/users/paginated")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 10
    assert data["users"][0]["username"] == "user0"
    assert data["total"] == 20

    # --- Cleanup mock ---
    app.dependency_overrides = {}

def test_deprecated_users_endpoint_limit():
    """
    Tests that the deprecated /users endpoint correctly applies the safety limit.
    """
    # --- Mock database dependency ---
    mock_db = MagicMock()
    mock_cursor = MagicMock()

    # Simulate more than 100 users in the database
    mock_users = []
    for i in range(150):
        mock_user = MagicMock(spec=sqlite3.Row)
        mock_user.keys.return_value = ["username", "email", "is_active"]
        mock_user.__getitem__.side_effect = {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "is_active": 1
        }.__getitem__
        mock_users.append(mock_user)

    def mock_execute(query):
        # This mock simulates the database returning only 100 users due to the LIMIT
        if "LIMIT 100" in query:
            mock_cursor.fetchall.return_value = mock_users[:100]
        else:
            mock_cursor.fetchall.return_value = mock_users

    mock_cursor.execute.side_effect = mock_execute
    mock_db.cursor.return_value = mock_cursor

    def override_get_db():
        try:
            yield mock_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # --- Test the deprecated endpoint ---
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 100

    # --- Cleanup mock ---
    app.dependency_overrides = {}
