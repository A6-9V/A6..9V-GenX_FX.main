import pytest

from api.routers.ea_http import ea_connections, pending_signals, trade_results


@pytest.fixture(autouse=True)
def clear_ea_http_state():
    """Clear global state in ea_http router before each test to ensure isolation."""
    ea_connections.clear()
    pending_signals.clear()
    trade_results.clear()
    yield
