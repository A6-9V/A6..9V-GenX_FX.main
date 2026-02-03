import time
import pandas as pd
import numpy as np
from utils.technical_indicators import TechnicalIndicators


def benchmark_support_resistance():
    ti = TechnicalIndicators()
    # Create a large dummy dataframe
    n = 10000
    df = pd.DataFrame(
        {
            "high": np.random.random(n) + 1,
            "low": np.random.random(n),
            "close": np.random.random(n) + 0.5,
            "volume": np.random.random(n) * 1000,
        }
    )

    # Warm up
    ti.add_support_resistance(df.head(100).copy())

    start_time = time.time()
    for _ in range(100):
        ti.add_support_resistance(df.copy())
    end_time = time.time()

    avg_time = (end_time - start_time) / 100
    print(f"Average time for add_support_resistance: {avg_time:.6f} seconds")


if __name__ == "__main__":
    benchmark_support_resistance()
