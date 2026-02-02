import pandas as pd
import numpy as np
from utils.technical_indicators import TechnicalIndicators

def test_wma_correctness():
    """Verify that WMA correctly weights recent prices more heavily."""
    ti = TechnicalIndicators()
    # P1=10, P2=20, P3=30, P4=40, P5=50
    df = pd.DataFrame({'close': [10.0, 20.0, 30.0, 40.0, 50.0]})
    # WMA(5) = (1*10 + 2*20 + 3*30 + 4*40 + 5*50) / (1+2+3+4+5)
    # = (10 + 40 + 90 + 160 + 250) / 15 = 550 / 15 = 36.666...
    result = ti.add_moving_averages(df)

    expected_wma = (1*10 + 2*20 + 3*30 + 4*40 + 5*50) / 15
    actual_wma = result['wma_5'].iloc[4]

    print(f"Expected WMA(5): {expected_wma:.4f}, Actual: {actual_wma:.4f}")
    assert np.isclose(actual_wma, expected_wma)

def test_obv_correctness():
    """Verify OBV calculation logic."""
    ti = TechnicalIndicators()
    df = pd.DataFrame({
        'close': [10, 12, 11, 11, 13],
        'volume': [100, 200, 150, 100, 300],
        'high': [11, 13, 12, 12, 14], # Needed for add_volume_indicators synthetic check
        'low': [9, 11, 10, 10, 12]
    })
    # OBV:
    # 0: base=0 (or usually 0 for first)
    # 1: close 12 > 10, OBV = 0 + 200 = 200
    # 2: close 11 < 12, OBV = 200 - 150 = 50
    # 3: close 11 == 11, OBV = 50 + 0 = 50
    # 4: close 13 > 11, OBV = 50 + 300 = 350

    result = ti.add_volume_indicators(df)
    actual_obv = result['obv'].tolist()
    expected_obv = [0, 200, 50, 50, 350]

    print(f"Expected OBV: {expected_obv}, Actual: {actual_obv}")
    assert actual_obv == expected_obv

def test_typical_price_reuse():
    """Verify typical_price is correctly calculated and reused."""
    ti = TechnicalIndicators()
    # Need 20 rows for CCI to trigger typical_price calculation
    df = pd.DataFrame({
        'high': [20] * 20,
        'low': [10] * 20,
        'close': [15] * 20
    })
    # Typical Price: (20+10+15)/3 = 45/3 = 15

    # add_momentum_indicators adds typical_price
    df = ti.add_momentum_indicators(df)
    assert 'typical_price' in df.columns
    assert np.allclose(df['typical_price'], [15] * 20)

    # add_support_resistance uses it
    df = ti.add_support_resistance(df)
    assert 'pivot' in df.columns
    assert np.allclose(df['pivot'], [15] * 20)

if __name__ == "__main__":
    try:
        test_wma_correctness()
        print("WMA Correctness: PASS")
        test_obv_correctness()
        print("OBV Correctness: PASS")
        test_typical_price_reuse()
        print("Typical Price Reuse: PASS")
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
