import pandas as pd
import numpy as np
import time

n = 100000
high = pd.Series(np.random.randn(n).cumsum())
low = pd.Series(np.random.randn(n).cumsum())
close = pd.Series(np.random.randn(n).cumsum())

def original():
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    return pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

def optimized():
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    return np.maximum(tr1, np.maximum(tr2, tr3))

# Warm up
original()
optimized()

start = time.time()
for _ in range(10): original()
print(f"Original: {time.time() - start:.4f}s")

start = time.time()
for _ in range(10): optimized()
print(f"Optimized: {time.time() - start:.4f}s")
