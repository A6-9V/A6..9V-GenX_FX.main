import pandas as pd
import numpy as np
import time

n = 100000
tr1 = pd.Series(np.random.randn(n))
tr2 = pd.Series(np.random.randn(n))
tr2.iloc[0] = np.nan
tr3 = pd.Series(np.random.randn(n))
tr3.iloc[0] = np.nan

def original():
    return pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

def optimized_fmax():
    return np.fmax(tr1, np.fmax(tr2, tr3))

# Warm up
original()
optimized_fmax()

start = time.time()
for _ in range(10): original()
print(f"Original: {time.time() - start:.4f}s")

start = time.time()
for _ in range(10): optimized_fmax()
print(f"Optimized fmax: {time.time() - start:.4f}s")

print(f"Verification: {np.allclose(original(), optimized_fmax(), equal_nan=True)}")
