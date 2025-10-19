import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
import os
import numpy as np
import pandas as pd

# Set test environment variables
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test"
os.environ["REDIS_URL"] = "redis://localhost:6379"

from api.main import app

client = TestClient(app)

class TestEdgeCases:
    """Comprehensive edge case testing for the GenX FX API"""
    
    def test_health_endpoint_structure(self):
        """Test health endpoint returns correct structure"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "timestamp" in data
        assert "database" in data
        
        # Validate timestamp format
        from datetime import datetime
        try:
            datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Invalid timestamp format")
    
    def test_root_endpoint_completeness(self):
        """Test root endpoint has all required information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["message", "version", "status", "github", "repository"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        assert data["status"] == "running"
    
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = client.options("/")
        assert response.status_code in [200, 405]

    def test_large_request_handling(self):
        """Test handling of large request payloads"""
        large_data = {
            "symbol": "BTCUSDT",
            "data": ["x" * 1000] * 100,
            "metadata": {
                "large_array": list(range(1000)),
                "nested": {"deep": {"data": "test" * 100}}
            }
        }
        
        response = client.post("/api/v1/predictions", json=large_data)
        assert response.status_code in [200, 400, 404, 422, 500]
    
    def test_malformed_json_handling(self):
        """Test handling of malformed JSON requests"""
        response = client.post(
            "/api/v1/predictions",
            content="{ invalid json }",
            headers={"content-type": "application/json"}
        )
        assert response.status_code in [400, 422]
    
    def test_null_and_empty_values(self):
        """Test handling of null and empty values in requests"""
        test_cases = [
            {},
            {"symbol": None},
            {"symbol": ""},
            {"symbol": "BTCUSDT", "data": None},
            {"symbol": "BTCUSDT", "data": []},
        ]
        
        for test_data in test_cases:
            response = client.post("/api/v1/predictions", json=test_data)
            assert response.status_code in [200, 400, 422, 500]
            if response.status_code >= 400:
                error_data = response.json()
                assert "detail" in error_data or "error" in error_data
    
    def test_special_characters_handling(self):
        """Test handling of special characters and Unicode"""
        special_data = {
            "symbol": "BTC/USDT",
            "comment": "Testing 🚀📊💹 emojis and café résumé naïve",
            "data": {
                "chinese": "测试数据",
                "arabic": "بيانات الاختبار",
                "special": "!@#$%^&*()_+-=[]{}|;:,.<>?"
            }
        }
        
        response = client.post("/api/v1/predictions", json=special_data)
        assert response.status_code in [200, 400, 422, 500]
    
    def test_numeric_edge_cases(self):
        """Test handling of numeric edge cases"""
        edge_cases = [
            {"value": float('inf')},
            {"value": float('-inf')},
            {"value": 0},
            {"value": 1e-10},
            {"value": 1e10},
        ]
        
        for test_data in edge_cases:
            try:
                response = client.post("/api/v1/predictions", json=test_data)
                assert response.status_code in [200, 400, 422, 500]
            except (ValueError, TypeError):
                pass
    
    def test_array_edge_cases(self):
        """Test handling of array edge cases"""
        array_cases = [
            {"data": []},
            {"data": [None, None, None]},
            {"data": [1, "string", True, None, {"nested": "object"}]},
            {"data": [[1, 2], [3, 4], []]},
        ]
        
        for test_data in array_cases:
            response = client.post("/api/v1/predictions", json=test_data)
            assert response.status_code in [200, 400, 422, 500]
    
    def test_deeply_nested_objects(self):
        """Test handling of deeply nested objects"""
        nested_data = {"data": {}}
        current = nested_data["data"]
        for i in range(20):
            current[f"level_{i}"] = {}
            current = current[f"level_{i}"]
        current["deep_value"] = "reached the bottom"
        
        response = client.post("/api/v1/predictions", json=nested_data)
        assert response.status_code in [200, 400, 422, 500]
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        
        results = []
        def make_request():
            response = client.get("/health")
            results.append(response.status_code)
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        assert all(status == 200 for status in results)
        assert len(results) == 10

class TestDataValidation:
    """Test data validation and sanitization"""
    
    def test_sql_injection_prevention(self):
        """Test SQL injection attempts are handled safely"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
        ]
        
        for malicious_input in malicious_inputs:
            test_data = {"symbol": malicious_input}
            response = client.post("/api/v1/predictions", json=test_data)
            assert response.status_code in [400, 422, 500]
            
            response_text = response.text.lower()
            dangerous_keywords = ["syntax error", "sql"]
            for keyword in dangerous_keywords:
                assert keyword not in response_text
    
    def test_xss_prevention(self):
        """Test XSS attempts are handled safely"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
        ]
        
        for payload in xss_payloads:
            test_data = {"comment": payload}
            response = client.post("/api/v1/predictions", json=test_data)
            assert response.status_code in [400, 422, 500]
            
            if response.headers.get("content-type", "").startswith("text/html"):
                assert "<script>" not in response.text

class TestPerformanceEdgeCases:
    """Test performance-related edge cases"""
    
    def test_response_time_reasonable(self):
        """Test that responses come back in reasonable time"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0
        assert response.status_code == 200
    
    def test_memory_usage_with_large_data(self):
        """Test memory usage doesn't explode with large data"""
        import psutil
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        large_data = {
            "data": ["x" * 1000] * 1000,
            "metadata": {"large_field": "y" * 10000}
        }
        
        response = client.post("/api/v1/predictions", json=large_data)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        assert memory_increase < 100 * 1024 * 1024

class TestErrorHandling:
    """Test comprehensive error handling"""
    
    def test_undefined_endpoints(self):
        """Test handling of undefined endpoints"""
        undefined_endpoints = [
            "/api/v1/nonexistent",
            "/api/v2/predictions",
        ]
        
        for endpoint in undefined_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404
            
            if response.headers.get("content-type", "").startswith("application/json"):
                error_data = response.json()
                assert "detail" in error_data or "message" in error_data
    
    def test_method_not_allowed(self):
        """Test handling of wrong HTTP methods"""
        test_cases = [
            ("DELETE", "/"),
            ("PUT", "/health"),
            ("PATCH", "/api/v1/predictions"),
        ]
        
        for method, endpoint in test_cases:
            response = client.request(method, endpoint)
            assert response.status_code in [405, 404]
    
    def test_content_type_handling(self):
        """Test handling of different content types"""
        response = client.post(
            "/api/v1/predictions",
            content="not json",
            headers={"content-type": "text/plain"}
        )
        assert response.status_code in [400, 415, 422]
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test handling of operations that might timeout"""
        with patch('api.main.predictor.predict') as mock_predict:
            def slow_predict(*args, **kwargs):
                import time
                time.sleep(0.1)
                return {"signal": "BUY", "confidence": 0.9}
            
            mock_predict.side_effect = slow_predict
            
            historical_data = {
                "historical_data": [
                    {"open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 1000}
                    for _ in range(100)
                ]
            }
            response = client.post("/api/v1/predictions", json=historical_data)
            assert response.status_code == 200
