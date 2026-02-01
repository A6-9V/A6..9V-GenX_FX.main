import os
import sys
import unittest

import numpy as np
import pandas as pd

# Add root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.technical_indicators import TechnicalIndicators


class TestTechnicalIndicatorsBolt(unittest.TestCase):
    def setUp(self):
        self.ti = TechnicalIndicators()
        np.random.seed(42)
        n = 100
        self.df = pd.DataFrame(
            {
                "open": np.random.randn(n) + 100,
                "high": np.random.randn(n) + 101,
                "low": np.random.randn(n) + 99,
                "close": np.random.randn(n) + 100,
                "volume": np.random.randint(100, 1000, n),
            }
        )

    def test_typical_price_reuse(self):
        # Initial run
        df_out = self.ti.add_all_indicators(self.df.copy())
        self.assertIn("typical_price", df_out.columns)
        self.assertIn("pivot", df_out.columns)
        # Check they are equal
        pd.testing.assert_series_equal(
            df_out["typical_price"], df_out["pivot"], check_names=False
        )

    def test_cci_calculation(self):
        df_out = self.ti.add_all_indicators(self.df.copy())
        self.assertIn("cci", df_out.columns)
        # Verify CCI is not all NaNs
        self.assertFalse(df_out["cci"].dropna().empty)

    def test_obv_calculation(self):
        df_out = self.ti.add_all_indicators(self.df.copy())
        self.assertIn("obv", df_out.columns)
        # Manual OBV check for first few rows
        close = self.df["close"]
        volume = self.df["volume"]
        expected_obv = [0.0] * len(self.df)
        for i in range(1, len(self.df)):
            if close[i] > close[i - 1]:
                expected_obv[i] = expected_obv[i - 1] + volume[i]
            elif close[i] < close[i - 1]:
                expected_obv[i] = expected_obv[i - 1] - volume[i]
            else:
                expected_obv[i] = expected_obv[i - 1]

        # Note: My optimized OBV uses np.sign and fillna(0)
        # Let's check if it matches
        np.testing.assert_array_almost_equal(df_out["obv"].values, expected_obv)

    def test_wma_calculation(self):
        df_out = self.ti.add_all_indicators(self.df.copy())
        self.assertIn("wma_20", df_out.columns)
        self.assertFalse(df_out["wma_20"].dropna().empty)


if __name__ == "__main__":
    unittest.main()
