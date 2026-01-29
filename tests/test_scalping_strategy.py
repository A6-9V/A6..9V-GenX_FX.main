
import pytest
import pandas as pd
import numpy as np
from core.strategies.scalping_strategy import ScalpingStrategy

def test_scalping_strategy_buy_signal():
    strategy = ScalpingStrategy()

    # Create mock data for a buy signal (50+ rows)
    n = 60
    data = {
        'close': [100.0] * n,
        'ema_5': [100.0] * n,
        'ema_13': [100.0] * n,
        'ema_50': [90.0] * n,
        'rsi': [60.0] * n
    }
    df = pd.DataFrame(data)

    # Set up crossover at the end
    df.loc[n-2, 'ema_5'] = 105.0
    df.loc[n-2, 'ema_13'] = 105.5
    df.loc[n-1, 'ema_5'] = 107.0
    df.loc[n-1, 'ema_13'] = 106.0

    result = strategy.analyze(df)

    assert result['signal'] == 'buy'
    assert result['confidence'] >= 0.8
    assert 'EMA Crossover' in result['reason']

def test_scalping_strategy_sell_signal():
    strategy = ScalpingStrategy()

    # Create mock data for a sell signal (50+ rows)
    n = 60
    data = {
        'close': [100.0] * n,
        'ema_5': [100.0] * n,
        'ema_13': [100.0] * n,
        'ema_50': [110.0] * n,
        'rsi': [40.0] * n
    }
    df = pd.DataFrame(data)

    # Set up crossover at the end
    df.loc[n-2, 'ema_5'] = 95.0
    df.loc[n-2, 'ema_13'] = 94.5
    df.loc[n-1, 'ema_5'] = 93.0
    df.loc[n-1, 'ema_13'] = 94.0

    result = strategy.analyze(df)

    assert result['signal'] == 'sell'
    assert result['confidence'] >= 0.8
    assert 'EMA Crossover' in result['reason']

def test_scalping_strategy_hold_signal():
    strategy = ScalpingStrategy()

    # Create mock data for no signal (50+ rows)
    n = 60
    data = {
        'close': [100.0] * n,
        'ema_5': [100.0] * n,
        'ema_13': [100.0] * n,
        'ema_50': [100.0] * n,
        'rsi': [50.0] * n
    }
    df = pd.DataFrame(data)

    result = strategy.analyze(df)

    assert result['signal'] == 'hold'
    assert result['confidence'] == 0.0
