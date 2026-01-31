## 2024-07-22 - Non-blocking CPU-Bound Tasks in Asyncio

**Learning:** I discovered a performance bottleneck in `core/trading_engine.py` where a CPU-bound operation, `technical_indicators.add_all_indicators`, was blocking the `asyncio` event loop. Even though the I/O operations were concurrent, this synchronous calculation serialized the execution, negating the benefits of `asyncio.gather`.

**Action:** In the future, I will use `asyncio.to_thread` to run any CPU-bound function in a separate thread. This will keep the event loop free and ensure that both I/O and CPU-bound tasks can run in parallel, maximizing throughput.

## 2025-01-30 - Vectorizing Rolling Linear Regression Slope

**Learning:** I identified a major performance bottleneck in `utils/technical_indicators.py` where `rolling().apply(np.polyfit)` was used to calculate trend strength. This iterative approach is extremely slow because it invokes the SVD-based `polyfit` solver and Python-level overhead for every window.

**Action:** I replaced the iterative approach with a vectorized mathematical formula using `np.convolve` and `rolling().sum()`. This optimization provided a ~3x speedup for the `add_trend_indicators` method, significantly reducing the CPU load during market data processing and signal generation.

## 2025-05-15 - Vectorizing Aroon with sliding_window_view

**Learning:** `pandas.rolling().apply(np.argmax)` is extremely slow for indicators like Aroon because it repeatedly calls a Python function for every window. Vectorizing this using `numpy.lib.stride_tricks.sliding_window_view` and `np.argmax(axis=1)` provides a ~250x speedup for the indicator calculation.

**Action:** Prefer `sliding_window_view` for any rolling window operation that requires custom aggregation functions (like argmax/argmin) which are not natively optimized in pandas.
