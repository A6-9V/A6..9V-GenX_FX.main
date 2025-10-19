import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
import os

# Set test environment variables
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test"
os.environ["REDIS_URL"] = "redis://localhost:6379"

# It's crucial to import the app after setting the environment variables
from api.main import app

client = TestClient(app)

class TestAPIEndpoints:
    """Tests for existing and stable API endpoints."""

    def test_root_endpoint_completeness(self):
        """Test root endpoint has all required information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()

        # Check for fields that actually exist in the response
        required_fields = ["message", "version", "status", "github", "repository"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Validate the content of the fields
        assert data["status"] == "running"
        assert "GenX-FX" in data["message"]

    def test_health_endpoint_structure(self):
        """Test the primary health endpoint for correct structure."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields for the simple health check
        assert "status" in data
        assert "database" in data
        assert "timestamp" in data
        assert data["status"] in ["healthy", "unhealthy"]

    def test_api_v1_health_endpoint_structure(self):
        """Test the v1 health endpoint for correct service structure."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()

        # Check required fields for the service-specific health check
        assert "status" in data
        assert "services" in data
        assert "ml_service" in data["services"]
        assert "data_service" in data["services"]
        assert "timestamp" in data
        
        # Validate timestamp format
        from datetime import datetime
        try:
            # Parse the ISO format timestamp
            datetime.fromisoformat(data["timestamp"])
        except (ValueError, TypeError):
            pytest.fail("Invalid timestamp format")

    def test_cors_headers(self):
        """Test CORS headers are properly set on a GET request."""
        # A GET request from a specific origin should have the correct headers.
        headers = {"Origin": "http://test.com"}
        response = client.get("/", headers=headers)
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        # Since allow_origins=["*"], the header should be "*"
        assert response.headers["access-control-allow-origin"] == "*"

    def test_concurrent_requests_to_health_endpoint(self):
        """Test handling of multiple concurrent requests."""
        import threading
        
        results = []
        def make_request():
            # Use a simple, fast endpoint for concurrency testing
            response = client.get("/health")
            results.append(response.status_code)
        
        # Create and start multiple threads
        threads = [threading.Thread(target=make_request) for _ in range(10)]
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should have succeeded
        assert all(status == 200 for status in results)
        assert len(results) == 10

class TestErrorHandling:
    """Tests for proper error handling, including undefined routes and methods."""

    def test_undefined_endpoints_return_404(self):
        """Test that requests to undefined endpoints return a 404 error."""
        undefined_endpoints = [
            "/api/v1/nonexistent",
            "/api/v2/some-route",
            "/this/does/not/exist",
        ]
        
        for endpoint in undefined_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404
            error_data = response.json()
            assert "detail" in error_data
            assert error_data["detail"] == "Not Found"

    def test_method_not_allowed_returns_405(self):
        """Test that using an incorrect HTTP method on an existing endpoint returns a 405 error."""
        # Define endpoints and the methods that are not allowed on them
        test_cases = [
            ("POST", "/"),
            ("PUT", "/health"),
            ("DELETE", "/api/v1/predictions"),
        ]
        
        for method, endpoint in test_cases:
            response = client.request(method, endpoint)
            assert response.status_code == 405
            error_data = response.json()
            assert "detail" in error_data
            assert "Method Not Allowed" in error_data["detail"]

class TestPerformance:
    """Basic performance checks for the API."""

    def test_health_check_response_time_is_reasonable(self):
        """Test that the health check response is returned within a reasonable time."""
        import time

        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response.status_code == 200
        # The response should be very fast, well under 1 second
        assert response_time < 1.0, f"Health check took too long: {response_time:.2f}s"

if __name__ == "__main__":
    # This allows running the test file directly
    pytest.main([__file__, "-v"])
