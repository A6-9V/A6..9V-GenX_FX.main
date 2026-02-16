import pytest

from api.routers import ea_http


@pytest.fixture(autouse=True)
def clear_ea_global_state():
    """
    Fixture to clear the global in-memory state in ea_http router between tests.
    Ensures test isolation for signals and connections.
    """
    ea_http.ea_connections.clear()
    ea_http.pending_signals.clear()
    ea_http.trade_results.clear()
    yield
