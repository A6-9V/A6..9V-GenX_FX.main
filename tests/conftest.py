import pytest

from api.routers.ea_http import ea_connections, pending_signals, trade_results


@pytest.fixture(autouse=True)
def clear_ea_state():
    """Clear the in-memory state of the EA router between tests"""
    ea_connections.clear()
    pending_signals.clear()
    trade_results.clear()
    yield
    ea_connections.clear()
    pending_signals.clear()
    trade_results.clear()
