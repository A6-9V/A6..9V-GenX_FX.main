import pytest
import os
from api.routers.ea_http import ea_connections, pending_signals, trade_results


@pytest.fixture(autouse=True)
def clear_ea_http_state():
    """Clear global state in ea_http router before each test"""
    ea_connections.clear()
    pending_signals.clear()
    trade_results.clear()


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup basic environment variables for tests"""
    # Ensure some required settings have values if not set
    if "EXNESS_LOGIN" not in os.environ:
        os.environ["EXNESS_LOGIN"] = "123456"
    if "EXNESS_PASSWORD" not in os.environ:
        os.environ["EXNESS_PASSWORD"] = "password"
    if "EXNESS_SERVER" not in os.environ:
        os.environ["EXNESS_SERVER"] = "Exness-MT5Trial8"
