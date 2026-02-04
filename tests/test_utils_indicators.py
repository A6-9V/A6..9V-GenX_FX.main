import pandas as pd
import numpy as np
import pytest
from utils.technical_indicators import TechnicalIndicators


def test_indicators_correctness():
    """Verify that indicators are calculated and have expected columns."""
    df = pd.DataFrame(
        {
            "open": [
                100.0,
                101.0,
                102.0,
                103.0,
                104.0,
                105.0,
                106.0,
                107.0,
                108.0,
                109.0,
            ]
            * 3,
            "high": [
                105.0,
                106.0,
                107.0,
                108.0,
                109.0,
                110.0,
                111.0,
                112.0,
                113.0,
                114.0,
            ]
            * 3,
            "low": [95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0, 102.0, 103.0, 104.0]
            * 3,
            "close": [
                102.0,
                103.0,
                104.0,
                105.0,
                106.0,
                107.0,
                108.0,
                109.0,
                110.0,
                111.0,
            ]
            * 3,
            "volume": [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900] * 3,
        }
    )

    ti = TechnicalIndicators()
    result = ti.add_all_indicators(df)

    # Check key indicators
    assert "rsi" in result.columns
    assert "macd" in result.columns
    assert "sma_20" in result.columns
    assert "ad_line" in result.columns
    assert "obv" in result.columns
    assert "vpt" in result.columns
    assert "pivot" in result.columns
    assert "r1" in result.columns
    assert "s1" in result.columns

    # Values should not be all NaN
    assert not result["rsi"].dropna().empty
    assert not result["ad_line"].dropna().empty
    assert not result["obv"].dropna().empty
    assert not result["pivot"].dropna().empty


def test_pivot_points_logic():
    """Verify pivot point calculation logic."""
    df = pd.DataFrame(
        {"high": [110.0], "low": [90.0], "close": [100.0], "volume": [1000]}
    )
    ti = TechnicalIndicators()
    res = ti.add_support_resistance(df)

    expected_pivot = (110.0 + 90.0 + 100.0) / 3.0
    assert res["pivot"].iloc[0] == pytest.approx(expected_pivot)
    assert res["r1"].iloc[0] == pytest.approx(2 * expected_pivot - 90.0)
    assert res["s1"].iloc[0] == pytest.approx(2 * expected_pivot - 110.0)


def test_obv_logic():
    """Verify OBV calculation logic."""
    df = pd.DataFrame(
        {"close": [100.0, 105.0, 103.0, 103.0], "volume": [1000, 1000, 1000, 1000]}
    )
    ti = TechnicalIndicators()
    res = ti.add_volume_indicators(df)

    # 1. 100.0 -> initial, 0
    # 2. 105.0 -> up, OBV = 1000
    # 3. 103.0 -> down, OBV = 1000 - 1000 = 0
    # 4. 103.0 -> same, OBV = 0

    # Wait, the current implementation of OBV in the file is:
    # price_change = df["close"].diff()
    # volume_direction = np.where(price_change > 0, df["volume"], np.where(price_change < 0, -df["volume"], 0))
    # df["obv"] = volume_direction.cumsum()
    # diff() gives NaN for the first element, so volume_direction[0] is 0 (if fillna is not used, but np.where treats NaN as False)

    # Let's check the result
    obv_vals = res["obv"].tolist()
    assert obv_vals[0] == 0
    assert obv_vals[1] == 1000
    assert obv_vals[2] == 0
    assert obv_vals[3] == 0


if __name__ == "__main__":
    pytest.main([__file__])
