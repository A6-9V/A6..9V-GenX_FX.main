import pandas as pd
import numpy as np
import pytest
import time
from utils.technical_indicators import TechnicalIndicators

def test_aroon_correctness():
    """Verify that the optimized Aroon calculation matches the expected logic."""
    # Create sample data
    n = 100
    df = pd.DataFrame({
        "open": np.random.randn(n).cumsum() + 100,
        "high": np.random.randn(n).cumsum() + 105,
        "low": np.random.randn(n).cumsum() + 95,
        "close": np.random.randn(n).cumsum() + 100,
        "volume": np.random.randint(1000, 5000, n)
    })

    ti = TechnicalIndicators()
    result = ti.add_trend_indicators(df.copy())

    assert "aroon_up" in result.columns
    assert "aroon_down" in result.columns
    assert "aroon_oscillator" in result.columns

    # Manual verification for a window
    period = 25
    for i in range(period - 1, n):
        window = df["high"].iloc[i - period + 1 : i + 1].values
        expected_argmax = np.argmax(window)
        expected_aroon_up = 100 * (period - expected_argmax) / period

        np.testing.assert_almost_equal(result["aroon_up"].iloc[i], expected_aroon_up)

def test_true_range_correctness():
    """Verify that the optimized True Range calculation matches the expected logic."""
    n = 50
    df = pd.DataFrame({
        "high": np.array([110, 112, 111, 115] * 13)[:n],
        "low": np.array([100, 102, 101, 103] * 13)[:n],
        "close": np.array([105, 104, 108, 107] * 13)[:n]
    })

    ti = TechnicalIndicators()
    result = ti.add_volatility_indicators(df.copy())

    assert "atr" in result.columns

    # Manual True Range calculation
    high = df["high"]
    low = df["low"]
    close_prev = df["close"].shift(1)

    tr1 = high - low
    tr2 = (high - close_prev).abs()
    tr3 = (low - close_prev).abs()
    expected_tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # In the optimized version, we use np.maximum which handles NaNs slightly differently or returns a numpy array
    # We check the ATR which is based on TR
    expected_atr = expected_tr.rolling(window=14).mean()

    np.testing.assert_array_almost_equal(result["atr"].dropna().values, expected_atr.dropna().values)

def test_performance_gains():
    """Document performance gains for the optimized indicators."""
    n = 5000
    df = pd.DataFrame({
        "high": np.random.randn(n).cumsum() + 100,
        "low": np.random.randn(n).cumsum() + 90,
        "close": np.random.randn(n).cumsum() + 95,
    })

    ti = TechnicalIndicators()

    # Measure ADX (includes True Range)
    start = time.time()
    ti._calculate_adx(df.copy())
    adx_time = time.time() - start
    print(f"\nADX calculation time (5000 points): {adx_time:.4f}s")

    # Measure Trend Indicators (includes Aroon)
    start = time.time()
    ti.add_trend_indicators(df.copy())
    trend_time = time.time() - start
    print(f"Trend indicators calculation time (5000 points): {trend_time:.4f}s")

    # These should be very fast now (usually < 0.1s for 5000 points)
    assert trend_time < 0.5
    assert adx_time < 0.5

if __name__ == "__main__":
    pytest.main([__file__])
