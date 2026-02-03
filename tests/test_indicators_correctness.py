import unittest
import pandas as pd
import numpy as np
from utils.technical_indicators import TechnicalIndicators


class TestTechnicalIndicatorsCorrectness(unittest.TestCase):
    def setUp(self):
        self.ti = TechnicalIndicators()

    def test_wma_correctness(self):
        # Data: [1, 2, 3, 4, 5, 6, 7], period: 5
        # Denominator = 5*6/2 = 15
        # WMA at index 4 (values [1, 2, 3, 4, 5]): (1*1 + 2*2 + 3*3 + 4*4 + 5*5) / 15 = (1+4+9+16+25)/15 = 55/15 = 3.666667
        # WMA at index 5 (values [2, 3, 4, 5, 6]): (2*1 + 3*2 + 4*3 + 5*4 + 6*5) / 15 = (2+6+12+20+30)/15 = 70/15 = 4.666667
        # WMA at index 6 (values [3, 4, 5, 6, 7]): (3*1 + 4*2 + 5*3 + 6*4 + 7*5) / 15 = (3+8+15+24+35)/15 = 85/15 = 5.666667
        df = pd.DataFrame({"close": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]})
        df = self.ti.add_moving_averages(df)

        expected_wma = [np.nan, np.nan, np.nan, np.nan, 55 / 15, 70 / 15, 85 / 15]
        np.testing.assert_array_almost_equal(df["wma_5"].values, expected_wma)

    def test_obv_correctness(self):
        # Price: [10, 11, 10, 10, 12], Volume: [100, 200, 300, 400, 500]
        # Diff: [NaN, 1, -1, 0, 2]
        # Dir: [0, 1, -1, 0, 1]
        # OBV: [0, 200, -100, -100, 400]
        df = pd.DataFrame(
            {
                "high": [10, 11, 10, 10, 12],
                "low": [10, 11, 10, 10, 12],
                "close": [10.0, 11.0, 10.0, 10.0, 12.0],
                "volume": [100.0, 200.0, 300.0, 400.0, 500.0],
            }
        )
        df = self.ti.add_volume_indicators(df)
        expected_obv = [0.0, 200.0, -100.0, -100.0, 400.0]
        np.testing.assert_array_almost_equal(df["obv"].values, expected_obv)

    def test_pivot_points_correctness(self):
        df = pd.DataFrame({"high": [10.0], "low": [5.0], "close": [9.0]})
        df = self.ti.add_support_resistance(df)

        pivot = (10 + 5 + 9) / 3  # 24/3 = 8
        r1 = 2 * 8 - 5  # 16 - 5 = 11
        s1 = 2 * 8 - 10  # 16 - 10 = 6
        r2 = 8 + (10 - 5)  # 8 + 5 = 13
        s2 = 8 - (10 - 5)  # 8 - 5 = 3

        self.assertEqual(df["pivot"].iloc[0], pivot)
        self.assertEqual(df["r1"].iloc[0], r1)
        self.assertEqual(df["s1"].iloc[0], s1)
        self.assertEqual(df["r2"].iloc[0], r2)
        self.assertEqual(df["s2"].iloc[0], s2)


if __name__ == "__main__":
    unittest.main()
