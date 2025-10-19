import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from api.services.trading_service import TradingService, TradeSignal, OrderRequest, SignalType, OrderType

@pytest.fixture
def trading_service():
    """Provides a new TradingService instance for each test."""
    return TradingService()

@pytest.mark.asyncio
async def test_initialization(trading_service: TradingService):
    """Test that the trading service initializes correctly."""
    await trading_service.initialize()
    assert trading_service.initialized is True

@pytest.mark.asyncio
async def test_get_active_signals(trading_service: TradingService):
    """Test retrieving active trading signals."""
    signals = await trading_service.get_active_signals()
    assert isinstance(signals, list)
    assert len(signals) > 0
    assert isinstance(signals[0], TradeSignal)

@pytest.mark.asyncio
async def test_create_signal(trading_service: TradingService):
    """Test creating a new trading signal."""
    signal = await trading_service.create_signal(
        symbol="ETHUSDT",
        signal_type=SignalType.SHORT,
        confidence=0.9,
        risk_params={}
    )
    assert isinstance(signal, TradeSignal)
    assert signal.symbol == "ETHUSDT"
    assert signal.signal_type == SignalType.SHORT

@pytest.mark.asyncio
async def test_place_order(trading_service: TradingService):
    """Test placing a trading order."""
    order_request = OrderRequest(
        symbol="BTCUSDT",
        order_type=OrderType.BUY,
        quantity=0.1
    )
    order_response = await trading_service.place_order(order_request)
    assert order_response.symbol == "BTCUSDT"
    assert order_response.quantity == 0.1

@pytest.mark.asyncio
async def test_get_order(trading_service: TradingService):
    """Test retrieving an order."""
    order = await trading_service.get_order("12345")
    assert order is not None
    assert order.order_id == "12345"

@pytest.mark.asyncio
async def test_cancel_order(trading_service: TradingService):
    """Test canceling an order."""
    result = await trading_service.cancel_order("12345")
    assert result is True

@pytest.mark.asyncio
async def test_get_portfolio_status(trading_service: TradingService):
    """Test retrieving portfolio status."""
    status = await trading_service.get_portfolio_status()
    assert status.total_balance > 0
