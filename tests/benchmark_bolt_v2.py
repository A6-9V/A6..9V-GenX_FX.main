import time
import numpy as np
import pandas as pd
import talib
from utils.technical_indicators import TechnicalIndicators
from api.services.scalping_service import ScalpingService

def benchmark_technical_indicators():
    print("Benchmarking TechnicalIndicators...")
    n = 1000
    data = {
        'open': np.random.random(n) + 1.0,
        'high': np.random.random(n) + 1.1,
        'low': np.random.random(n) + 0.9,
        'close': np.random.random(n) + 1.0,
        'volume': np.random.random(n) * 1000
    }
    df = pd.DataFrame(data)
    ti = TechnicalIndicators()

    # Measure add_all_indicators
    start = time.time()
    for _ in range(50):
        ti.add_all_indicators(df)
    end = time.time()
    total_time = end - start
    print(f"Total time for 50 calls to add_all_indicators: {total_time:.4f}s ({total_time/50:.4f}s per call)")

    # Specific measure for Parabolic SAR
    start = time.time()
    for _ in range(100):
        ti._calculate_parabolic_sar(df)
    end = time.time()
    sar_time = end - start
    print(f"Time for 100 calls to _calculate_parabolic_sar: {sar_time:.4f}s")

def benchmark_scalping_service():
    print("\nBenchmarking ScalpingService...")
    n = 500
    data = {
        'open': np.random.random(n) + 1.0,
        'high': np.random.random(n) + 1.1,
        'low': np.random.random(n) + 0.9,
        'close': np.random.random(n) + 1.0,
        'volume': np.random.random(n) * 1000
    }
    df = pd.DataFrame(data)
    ss = ScalpingService()

    # Measure _analyze_5m
    start = time.time()
    for _ in range(500):
        ss._analyze_5m(df)
    end = time.time()
    analyze_5m_time = end - start
    print(f"Time for 500 calls to _analyze_5m: {analyze_5m_time:.4f}s")

if __name__ == "__main__":
    benchmark_technical_indicators()
    benchmark_scalping_service()
