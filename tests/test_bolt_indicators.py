import numpy as np
import pandas as pd
import pytest

from utils.technical_indicators import TechnicalIndicators


def test_add_all_indicators_correctness():
    ti = TechnicalIndicators()
    n = 100
    df = pd.DataFrame(
        {
            "high": np.linspace(102, 110, n),
            "low": np.linspace(98, 106, n),
            "close": np.linspace(100, 108, n),
            "volume": np.ones(n) * 1000,
        }
    )

    result = ti.add_all_indicators(df)

    # Check if typical_price is present and correct
    assert "typical_price" in result.columns
    expected_tp = (df["high"] + df["low"] + df["close"]) / 3
    pd.testing.assert_series_equal(
        result["typical_price"], expected_tp, check_names=False
    )

    # Check if Pivot Points are present and correct
    assert "pivot" in result.columns
    pd.testing.assert_series_equal(result["pivot"], expected_tp, check_names=False)

    # Check if CCI is present
    assert "cci" in result.columns

    # Check if WMA is present and reasonably valued
    assert "wma_20" in result.columns
    # The last WMA_20 should be greater than the first one if prices are increasing
    assert result["wma_20"].iloc[-1] > result["wma_20"].iloc[20]


def test_wma_logic():
    ti = TechnicalIndicators()
    # Simple case: 3 periods
    df = pd.DataFrame({"close": [10.0, 20.0, 30.0, 40.0, 50.0]})
    # We need to mock add_moving_averages periods to include 3, or just test the logic
    # Since add_moving_averages uses fixed periods [5, 10, 20, 50, 100, 200]
    # let's use 5
    df = pd.DataFrame({"close": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]})
    result = ti.add_moving_averages(df)

    # WMA 5 for [10, 20, 30, 40, 50]
    # Weights: [1, 2, 3, 4, 5], Sum: 15
    # Expected: (10*1 + 20*2 + 30*3 + 40*4 + 50*5) / 15 = (10+40+90+160+250)/15 = 550/15 = 36.666...
    assert pytest.approx(result["wma_5"].iloc[4]) == 550 / 15

    # WMA 5 for [20, 30, 40, 50, 60]
    # Expected: (20*1 + 30*2 + 40*3 + 50*4 + 60*5) / 15 = (20+60+120+200+300)/15 = 700/15 = 46.666...
    assert pytest.approx(result["wma_5"].iloc[5]) == 700 / 15


def test_ad_line_logic():
    ti = TechnicalIndicators()
    df = pd.DataFrame(
        {
            "high": [110, 120],
            "low": [100, 100],
            "close": [105, 115],
            "volume": [1000, 1000],
        }
    )
    result = ti.add_volume_indicators(df)

    # Row 0: H=110, L=100, C=105, V=1000
    # Range = 10
    # MFM = (2*105 - 100 - 110) / 10 = (210 - 210) / 10 = 0
    # AD = 0
    assert result["ad_line"].iloc[0] == 0

    # Row 1: H=120, L=100, C=115, V=1000
    # Range = 20
    # MFM = (2*115 - 100 - 120) / 20 = (230 - 220) / 20 = 10 / 20 = 0.5
    # MFV = 0.5 * 1000 = 500
    # AD = 0 + 500 = 500
    assert result["ad_line"].iloc[1] == 500


def test_stoch_and_williams_logic():
    ti = TechnicalIndicators()
    # 14 rows with same values
    df = pd.DataFrame(
        {
            "high": [110] * 14,
            "low": [100] * 14,
            "close": [105] * 14,
        }
    )
    # Add one row that changes range
    df.loc[14] = [120, 100, 110]

    result = ti.add_momentum_indicators(df)

    # At index 14: High=120, Low=100, Close=110
    # Range = 20
    # Stoch_K = 100 * (110 - 100) / 20 = 100 * 10 / 20 = 50
    assert result["stoch_k"].iloc[14] == 50
    # Williams_R = -100 * (120 - 110) / 20 = -100 * 10 / 20 = -50
    assert result["williams_r"].iloc[14] == -50


def test_donchian_logic():
    ti = TechnicalIndicators()
    # 20 rows
    df = pd.DataFrame(
        {
            "high": np.linspace(110, 120, 20),
            "low": np.linspace(90, 100, 20),
            "close": np.linspace(100, 110, 20),
        }
    )
    result = ti.add_volatility_indicators(df)

    # At index 19:
    # Upper = max(high) = 120
    # Lower = min(low) = 90
    # Middle = (120 + 90) / 2 = 105
    # Position = (110 - 90) / (120 - 90) = 20 / 30 = 0.666...
    assert result["donchian_upper"].iloc[19] == 120
    assert result["donchian_lower"].iloc[19] == 90
    assert result["donchian_middle"].iloc[19] == 105
    assert pytest.approx(result["donchian_position"].iloc[19]) == 20/30


def test_obv_vpt_logic():
    ti = TechnicalIndicators()
    df = pd.DataFrame(
        {
            "high": [100, 110, 105], # Needed for synthetic volume check
            "low": [100, 110, 105],
            "close": [100, 110, 105],
            "volume": [1000, 1000, 1000],
        }
    )
    result = ti.add_volume_indicators(df)

    # OBV:
    # idx 0: 0
    # idx 1: Price up, OBV = 1000
    # idx 2: Price down, OBV = 1000 - 1000 = 0
    assert result["obv"].iloc[1] == 1000
    assert result["obv"].iloc[2] == 0

    # VPT:
    # idx 1: change = (110-100)/100 = 0.1. VPT = 0.1 * 1000 = 100
    # idx 2: change = (105-110)/110 = -5/110. VPT = 100 + (-5/110 * 1000) = 100 - 45.45... = 54.54...
    assert result["vpt"].iloc[1] == pytest.approx(100)
    assert result["vpt"].iloc[2] == pytest.approx(100 + (-5/110 * 1000))


if __name__ == "__main__":
    pytest.main([__file__])
