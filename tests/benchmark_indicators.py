import time

import numpy as np
import pandas as pd

from utils.technical_indicators import TechnicalIndicators


def benchmark():
    # Create a much larger sample dataframe
    size = 100000
    df = pd.DataFrame(
        {
            "open": np.random.randn(size) + 100,
            "high": np.random.randn(size) + 101,
            "low": np.random.randn(size) + 99,
            "close": np.random.randn(size) + 100,
            "volume": np.random.randint(100, 1000, size),
        }
    )

    ti = TechnicalIndicators()

    print(f"Starting benchmark for {size} rows...")

    # Measure individual methods
    methods = [
        ti.add_moving_averages,
        ti.add_momentum_indicators,
        ti.add_volatility_indicators,
        ti.add_volume_indicators,
        ti.add_trend_indicators,
        ti.add_support_resistance,
    ]

    total_start = time.time()
    for method in methods:
        start = time.time()
        method(df.copy())
        print(f"{method.__name__}: {time.time() - start:.4f} seconds")
    print(f"Total time: {time.time() - total_start:.4f} seconds")


if __name__ == "__main__":
    benchmark()
