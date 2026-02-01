## 2024-07-22 - Non-blocking CPU-Bound Tasks in Asyncio

**Learning:** I discovered a performance bottleneck in `core/trading_engine.py` where a CPU-bound operation, `technical_indicators.add_all_indicators`, was blocking the `asyncio` event loop. Even though the I/O operations were concurrent, this synchronous calculation serialized the execution, negating the benefits of `asyncio.gather`.

**Action:** In the future, I will use `asyncio.to_thread` to run any CPU-bound function in a separate thread. This will keep the event loop free and ensure that both I/O and CPU-bound tasks can run in parallel, maximizing throughput.

## 2025-01-30 - Vectorizing Rolling Linear Regression Slope

**Learning:** I identified a major performance bottleneck in `utils/technical_indicators.py` where `rolling().apply(np.polyfit)` was used to calculate trend strength. This iterative approach is extremely slow because it invokes the SVD-based `polyfit` solver and Python-level overhead for every window.

**Action:** I replaced the iterative approach with a vectorized mathematical formula using `np.convolve` and `rolling().sum()`. This optimization provided a ~3x speedup for the `add_trend_indicators` method, significantly reducing the CPU load during market data processing and signal generation.

## 2025-01-30 - Row-wise Maximum and Arithmetic Overhead

**Learning:** I identified a significant performance bottleneck in the ADX calculation within `utils/technical_indicators.py`. Specifically, using `pd.concat([...], axis=1).max(axis=1)` to calculate the True Range (TR) is extremely inefficient compared to nested `np.maximum` calls. Additionally, performing row-wise arithmetic on Pandas Series carries substantial overhead for index alignment and validation.

**Action:** I replaced `pd.concat().max()` with nested `np.maximum` and moved arithmetic operations to raw NumPy arrays by using `.values`. This combination reduced the ADX calculation time by ~43%, demonstrating that bypassing the Pandas Series abstraction for simple row-wise math is a powerful optimization in hot code paths.

## 2025-01-31 - Vectorizing Sliding Window Sequence Creation

**Learning:** I identified a major performance bottleneck in `ai_models/feature_engineer.py` where manual Python loops were used to create sliding window sequences and normalized "chart images" for ML models. These loops involved repeated slicing and redundant `min()`/`max()` calculations on Pandas DataFrames, which is extremely slow for large datasets.

**Action:** I replaced the manual loops with vectorized NumPy operations using `np.lib.stride_tricks.sliding_window_view`. This optimization provided a ~90x speedup for `_create_chart_images` and a ~400x speedup for `_create_price_sequences`, dramatically reducing the feature engineering time during both training and prediction. I also added length checks to maintain the original behavior for inputs shorter than the window size, avoiding `ValueError` from the NumPy function.
