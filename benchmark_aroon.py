import pandas as pd
import numpy as np
import time

def aroon_original(df, period=25):
    aroon_up = (
        100
        * (period - df["high"].rolling(window=period).apply(np.argmax))
        / period
    )
    aroon_down = (
        100
        * (period - df["low"].rolling(window=period).apply(np.argmin))
        / period
    )
    return aroon_up, aroon_down

def aroon_optimized(df, period=25):
    high_np = df["high"].to_numpy()
    low_np = df["low"].to_numpy()

    shape = (high_np.shape[0] - period + 1, period)
    strides = (high_np.strides[0], high_np.strides[0])

    rolling_highs = np.lib.stride_tricks.as_strided(
        high_np, shape=shape, strides=strides
    )
    rolling_lows = np.lib.stride_tricks.as_strided(
        low_np, shape=shape, strides=strides
    )

    argmax_highs = np.argmax(rolling_highs, axis=1)
    argmin_lows = np.argmin(rolling_lows, axis=1)

    aroon_up_values = 100 * (period - argmax_highs) / period
    aroon_down_values = 100 * (period - argmin_lows) / period

    aroon_up = pd.Series(aroon_up_values, index=df.index[period - 1 :])
    aroon_down = pd.Series(aroon_down_values, index=df.index[period - 1 :])

    return aroon_up, aroon_down

# Generate dummy data
n = 10000
df = pd.DataFrame({
    "high": np.random.randn(n).cumsum(),
    "low": np.random.randn(n).cumsum(),
})

# Benchmark original
start = time.time()
up1, down1 = aroon_original(df)
end = time.time()
orig_time = end - start
print(f"Original time: {orig_time:.4f}s")

# Benchmark optimized
start = time.time()
up2, down2 = aroon_optimized(df)
end = time.time()
opt_time = end - start
print(f"Optimized time: {opt_time:.4f}s")
print(f"Speedup: {orig_time / opt_time:.1f}x")

# Verify equivalence of values
np.testing.assert_array_almost_equal(up1.dropna().values, up2.values)
np.testing.assert_array_almost_equal(down1.dropna().values, down2.values)
print("Verification successful!")
