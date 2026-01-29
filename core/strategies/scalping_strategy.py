"""
Scalping Strategy for GenX FX Trading System
Optimized for 5m, 15m, and 30m timeframes
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ScalpingStrategy:
    """
    A robust scalping strategy using multiple EMA crossovers and RSI confirmation.
    Designed for small timeframes (5m, 15m, 30m).
    """

    def __init__(self,
                 fast_ema: int = 5,
                 medium_ema: int = 13,
                 slow_ema: int = 50,
                 rsi_period: int = 14,
                 rsi_overbought: int = 70,
                 rsi_oversold: int = 30):
        self.fast_ema = fast_ema
        self.medium_ema = medium_ema
        self.slow_ema = slow_ema
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold

    def analyze(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Analyzes the data and returns a signal.

        Args:
            df: DataFrame with OHLCV data and indicators.
                Required columns: 'close', 'ema_5', 'ema_13', 'ema_50', 'rsi'
                Note: Indicators should be pre-calculated.

        Returns:
            A dictionary containing the signal ('buy', 'sell', or 'hold') and confidence.
        """
        try:
            if df is None or len(df) < self.slow_ema:
                return {"signal": "hold", "confidence": 0.0, "reason": "Insufficient data"}

            latest = df.iloc[-1]
            prev = df.iloc[-2]

            # Check if required columns exist, if not, we can't proceed
            required_cols = [f'ema_{self.fast_ema}', f'ema_{self.medium_ema}', f'ema_{self.slow_ema}', 'rsi']
            for col in required_cols:
                if col not in df.columns:
                    return {"signal": "hold", "confidence": 0.0, "reason": f"Missing column: {col}"}

            fast = latest[f'ema_{self.fast_ema}']
            medium = latest[f'ema_{self.medium_ema}']
            slow = latest[f'ema_{self.slow_ema}']
            rsi = latest['rsi']

            prev_fast = prev[f'ema_{self.fast_ema}']
            prev_medium = prev[f'ema_{self.medium_ema}']

            signal = "hold"
            confidence = 0.0
            reason = "No clear setup"

            # Long Setup: EMA 5 crosses above EMA 13, and both are above EMA 50. RSI > 50.
            if fast > medium and prev_fast <= prev_medium and medium > slow and rsi > 50:
                signal = "buy"
                confidence = 0.8
                reason = "EMA Crossover (Up) + RSI Confirmation"
            # Short Setup: EMA 5 crosses below EMA 13, and both are below EMA 50. RSI < 50.
            elif fast < medium and prev_fast >= prev_medium and medium < slow and rsi < 50:
                signal = "sell"
                confidence = 0.8
                reason = "EMA Crossover (Down) + RSI Confirmation"

            # Strength adjustment based on RSI
            if signal == "buy":
                if rsi > 60:
                    confidence += 0.1
                if latest['close'] > latest[f'ema_{self.fast_ema}']:
                    confidence += 0.05
            elif signal == "sell":
                if rsi < 40:
                    confidence += 0.1
                if latest['close'] < latest[f'ema_{self.fast_ema}']:
                    confidence += 0.05

            return {
                "signal": signal,
                "confidence": min(confidence, 1.0),
                "reason": reason,
                "indicators": {
                    "fast_ema": fast,
                    "medium_ema": medium,
                    "slow_ema": slow,
                    "rsi": rsi
                }
            }

        except Exception as e:
            logger.error(f"Error in ScalpingStrategy.analyze: {e}")
            return {"signal": "hold", "confidence": 0.0, "reason": f"Error: {str(e)}"}
