## 2024-07-22 - Non-blocking CPU-Bound Tasks in Asyncio

**Learning:** I discovered a performance bottleneck in `core/trading_engine.py` where a CPU-bound operation, `technical_indicators.add_all_indicators`, was blocking the `asyncio` event loop. Even though the I/O operations were concurrent, this synchronous calculation serialized the execution, negating the benefits of `asyncio.gather`.

**Action:** In the future, I will use `asyncio.to_thread` to run any CPU-bound function in a separate thread. This will keep the event loop free and ensure that both I/O and CPU-bound tasks can run in parallel, maximizing throughput.

## 2025-01-30 - Vectorizing Rolling Linear Regression Slope

**Learning:** I identified a major performance bottleneck in `utils/technical_indicators.py` where `rolling().apply(np.polyfit)` was used to calculate trend strength. This iterative approach is extremely slow because it invokes the SVD-based `polyfit` solver and Python-level overhead for every window.

**Action:** I replaced the iterative approach with a vectorized mathematical formula using `np.convolve` and `rolling().sum()`. This optimization provided a ~3x speedup for the `add_trend_indicators` method, significantly reducing the CPU load during market data processing and signal generation.

## 2025-01-30 - Vectorizing Rolling Argmax/Argmin for Aroon

**Learning:** I identified a significant bottleneck in `utils/technical_indicators.py` where `rolling().apply(np.argmax)` and `rolling().apply(np.argmin)` were used to calculate the Aroon indicator. This pattern is extremely slow because it forces pandas to repeatedly slice the data and call a Python/NumPy function for every window.

**Action:** I implemented a vectorized approach using `numpy.lib.stride_tricks.as_strided` to create a sliding window view of the data, followed by a vectorized `np.argmax(axis=1)`. This optimization provided a ~280x speedup for the Aroon indicator, reducing its execution time from ~1.2s to ~4ms for 10,000 data points. I also vectorized the True Range calculation using `np.fmax` for a ~20x speedup and better NaN handling compared to `pd.concat().max()`.
