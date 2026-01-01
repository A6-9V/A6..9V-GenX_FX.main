import pytest
import asyncio
from unittest.mock import Mock, patch
import os
import sqlite3
import time
from api import main as api_main

# Skip tests if FastAPI is not available
try:
    from fastapi.testclient import TestClient
    from api.main import app, get_db
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

if FASTAPI_AVAILABLE:
    from fastapi.testclient import TestClient
    # Set test environment variables
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
    os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test"
    os.environ["REDIS_URL"] = "redis://localhost:6379"
else:
    client = None

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_auth():
    """Mock authentication"""
    with patch('api.utils.auth.get_current_user') as mock_user:
        mock_user.return_value = {"username": "testuser"}
        yield mock_user

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint(client):
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

def test_get_trading_pairs(client):
    """Test the /trading-pairs endpoint"""

    # Mock database connection
    def get_test_db():
        try:
            db = sqlite3.connect(":memory:", check_same_thread=False)
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(
                """
                CREATE TABLE trading_pairs (
                    symbol TEXT,
                    base_currency TEXT,
                    quote_currency TEXT,
                    is_active INTEGER
                )
            """
            )
            cursor.execute(
                "INSERT INTO trading_pairs VALUES ('BTCUSD', 'BTC', 'USD', 1)"
            )
            db.commit()
            yield db
        finally:
            db.close()

    # Override the dependency with the test database
    app.dependency_overrides[get_db] = get_test_db

    response = client.get("/trading-pairs")
    assert response.status_code == 200
    data = response.json()
    assert "trading_pairs" in data
    assert len(data["trading_pairs"]) == 1
    assert data["trading_pairs"][0]["symbol"] == "BTCUSD"


def test_get_trading_pairs_caching(client):
    """Test the caching behavior of the /trading-pairs endpoint"""

    # Manually reset cache state before the test run
    api_main._trading_pairs_cache = None
    api_main._trading_pairs_cache_timestamp = None

    # Mock database connection with a cursor that can be spied on
    class MockCursor:
        def __init__(self):
            self.execute_count = 0

        def execute(self, *args, **kwargs):
            self.execute_count += 1

        def fetchall(self):
            # This is what the real cursor's fetchall would return
            # after a successful execute.
            if self.execute_count > 0:
                return [
                    {
                        "symbol": "BTCUSD",
                        "base_currency": "BTC",
                        "quote_currency": "USD",
                    }
                ]
            return []

    class MockConnection:
        def __init__(self):
            self.cursor_instance = MockCursor()

        def cursor(self):
            return self.cursor_instance

        def close(self):
            pass

    mock_db = MockConnection()

    def get_mock_db():
        yield mock_db

    # Override the dependency
    app.dependency_overrides[get_db] = get_mock_db

    # --- First call - should hit the database ---
    response1 = client.get("/trading-pairs")
    assert response1.status_code == 200
    assert mock_db.cursor_instance.execute_count == 1

    # --- Second call - should be cached ---
    response2 = client.get("/trading-pairs")
    assert response2.status_code == 200
    assert mock_db.cursor_instance.execute_count == 1  # Should not have incremented

    # --- Wait for cache to expire ---
    # To test expiration, we would need to manipulate the CACHE_DURATION
    # or mock `datetime.now()`, which is more complex. For this test,
    # we'll just verify the immediate caching behavior.

    # --- Clear the override ---
    app.dependency_overrides.clear()
