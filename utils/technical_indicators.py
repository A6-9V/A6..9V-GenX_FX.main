"""
Technical Indicators Utility
Comprehensive technical analysis indicators for forex trading
"""

import logging
from typing import Dict, Optional

import numpy as np
import pandas as pd
import talib

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """
    Comprehensive technical indicators calculator
    Optimized for forex trading signal generation
    """

    def __init__(self):
        self.indicators = {}
        logger.debug("Technical Indicators utility initialized")

    def add_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add all technical indicators to the dataframe"""
        try:
            # Make a copy to avoid modifying original data
            data = df.copy()

            # Pre-calculate common intermediate results to avoid redundant work
            # in sub-methods. Saving as a column for easy reuse across indicators.
            # ⚡ Bolt: Use raw numpy values to bypass series arithmetic overhead
            data["typical_price"] = (
                data["high"].values + data["low"].values + data["close"].values
            ) / 3

            # Price-based indicators
            data = self.add_moving_averages(data)
            data = self.add_momentum_indicators(data)
            data = self.add_volatility_indicators(data)
            data = self.add_volume_indicators(data)
            data = self.add_trend_indicators(data)
            data = self.add_support_resistance(data)

            logger.debug(
                f"Added {len(data.columns) - len(df.columns)} technical indicators"
            )
            return data

        except Exception as e:
            logger.error(f"Error adding technical indicators: {e}")
            return df

    def add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add moving average indicators"""
        try:
            periods = [5, 10, 20, 50, 100, 200]

            # ⚡ Bolt: Convert to float64 for TA-Lib
            close_vals = df["close"].values.astype(np.float64)
            for period in periods:
                if len(df) >= period:
                    # Simple Moving Average (Optimized: TA-Lib)
                    # ⚡ Bolt: Using talib.SMA is ~10x faster than np.convolve
                    df[f"sma_{period}"] = talib.SMA(close_vals, timeperiod=period)

                    # Exponential Moving Average (Optimized: TA-Lib)
                    df[f"ema_{period}"] = talib.EMA(close_vals, timeperiod=period)

                    # Weighted Moving Average (Optimized: TA-Lib)
                    df[f"wma_{period}"] = talib.WMA(close_vals, timeperiod=period)

            # Moving Average Convergence Divergence (MACD) (Optimized: TA-Lib)
            if len(df) >= 26:
                macd, macdsignal, macdhist = talib.MACD(
                    close_vals, fastperiod=12, slowperiod=26, signalperiod=9
                )
                df["macd"] = macd
                df["macd_signal"] = macdsignal
                df["macd_histogram"] = macdhist

            return df

        except Exception as e:
            logger.error(f"Error adding moving averages: {e}")
            return df

    def add_momentum_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add momentum-based indicators"""
        try:
            # ⚡ Bolt: Extract raw values for TA-Lib
            high_vals = df["high"].values.astype(np.float64)
            low_vals = df["low"].values.astype(np.float64)
            close_vals = df["close"].values.astype(np.float64)

            # Relative Strength Index (RSI) (Optimized: TA-Lib)
            if len(df) >= 14:
                # ⚡ Bolt: talib.RSI uses Wilder's smoothing and is much faster
                df["rsi"] = talib.RSI(close_vals, timeperiod=14)

            # Stochastic Oscillator & Williams %R (Optimized: TA-Lib)
            if len(df) >= 14:
                # Stochastic Oscillator (Fast)
                fastk, fastd = talib.STOCHF(
                    high_vals,
                    low_vals,
                    close_vals,
                    fastk_period=14,
                    fastd_period=3,
                    fastd_matype=0,
                )
                df["stoch_k"] = fastk
                df["stoch_d"] = fastd

                # Williams %R
                df["williams_r"] = talib.WILLR(
                    high_vals, low_vals, close_vals, timeperiod=14
                )

            # Rate of Change (ROC) (Optimized: TA-Lib)
            periods = [5, 10, 20]
            for period in periods:
                if len(df) >= period:
                    # ⚡ Bolt: Using talib.ROC is faster and handles NaN correctly
                    df[f"roc_{period}"] = talib.ROC(close_vals, timeperiod=period)

            # Commodity Channel Index (CCI) (Optimized: TA-Lib)
            if len(df) >= 20:
                # ⚡ Bolt: talib.CCI is much faster than manual mean deviation calculation
                df["cci"] = talib.CCI(high_vals, low_vals, close_vals, timeperiod=20)

            return df

        except Exception as e:
            logger.error(f"Error adding momentum indicators: {e}")
            return df

    def add_volatility_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volatility-based indicators"""
        try:
            # ⚡ Bolt: Extract raw values for TA-Lib
            high_vals = df["high"].values.astype(np.float64)
            low_vals = df["low"].values.astype(np.float64)
            close_vals = df["close"].values.astype(np.float64)

            # Average True Range (ATR) (Optimized: TA-Lib)
            if len(df) >= 14:
                # ⚡ Bolt: Using talib.ATR is much faster than manual TR/ATR calculation
                # Note: standard ATR uses Wilder's smoothing
                df["atr"] = talib.ATR(high_vals, low_vals, close_vals, timeperiod=14)

            # Bollinger Bands (Optimized: TA-Lib)
            if len(df) >= 20:
                # ⚡ Bolt: Using talib.BBANDS is significantly faster
                upper, middle, lower = talib.BBANDS(
                    close_vals, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
                )
                df["bb_upper"] = upper
                df["bb_lower"] = lower
                df["bb_middle"] = middle
                width = upper - lower
                df["bb_width"] = width
                df["bb_position"] = (close_vals - lower) / width

            # Volatility indicators (Optimized: TA-Lib)
            periods = [10, 20, 50, 100]
            for period in periods:
                if len(df) >= period:
                    # ⚡ Bolt: talib.STDDEV is faster than manual rolling variance
                    vol_vals = talib.STDDEV(close_vals, timeperiod=period, nbdev=1)
                    df[f"volatility_{period}"] = vol_vals
                    df[f"volatility_ratio_{period}"] = vol_vals / close_vals

            # Donchian Channels (Keep existing vectorized logic as TA-Lib doesn't have it)
            if len(df) >= 20:
                high_windows_20 = np.lib.stride_tricks.sliding_window_view(
                    high_vals, 20
                )
                low_windows_20 = np.lib.stride_tricks.sliding_window_view(low_vals, 20)

                d_upper_vals = np.full(len(df), np.nan)
                d_lower_vals = np.full(len(df), np.nan)

                d_upper_vals[20 - 1 :] = np.max(high_windows_20, axis=1)
                d_lower_vals[20 - 1 :] = np.min(low_windows_20, axis=1)

                df["donchian_upper"] = d_upper_vals
                df["donchian_lower"] = d_lower_vals
                df["donchian_middle"] = (d_upper_vals + d_lower_vals) / 2
                df["donchian_position"] = (close_vals - d_lower_vals) / (
                    d_upper_vals - d_lower_vals
                )

            return df

        except Exception as e:
            logger.error(f"Error adding volatility indicators: {e}")
            return df

    def add_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volume-based indicators"""
        try:
            if "volume" not in df.columns or df["volume"].sum() == 0:
                # Create synthetic volume for forex data
                df["volume"] = (df["high"] - df["low"]) * 1000000

            # ⚡ Bolt: Extract raw values for TA-Lib
            high_vals = df["high"].values.astype(np.float64)
            low_vals = df["low"].values.astype(np.float64)
            close_vals = df["close"].values.astype(np.float64)
            volume_vals = df["volume"].values.astype(np.float64)

            # Volume Moving Averages (Optimized: TA-Lib)
            periods = [10, 20, 50]
            for period in periods:
                if len(df) >= period:
                    # ⚡ Bolt: talib.SMA is much faster for volume averages
                    v_sma = talib.SMA(volume_vals, timeperiod=period)
                    df[f"volume_sma_{period}"] = v_sma
                    df[f"volume_ratio_{period}"] = volume_vals / v_sma

            # On-Balance Volume (OBV) (Optimized: TA-Lib)
            if len(df) >= 2:
                # ⚡ Bolt: talib.OBV is significantly faster than manual cumulative sum
                obv_vals = talib.OBV(close_vals, volume_vals)
                # ⚡ Bolt: Align with previous behavior (starting at 0 for compatibility)
                df["obv"] = obv_vals - obv_vals[0]

            # Volume Price Trend (VPT) (Keep existing vectorized logic as TA-Lib doesn't have it)
            if len(df) >= 2:
                pct_change = np.zeros_like(close_vals)
                with np.errstate(divide="ignore", invalid="ignore"):
                    pct_change[1:] = np.diff(close_vals) / close_vals[:-1]
                df["vpt"] = (pct_change * volume_vals).cumsum()

            # Accumulation/Distribution Line (Optimized: TA-Lib)
            if len(df) >= 1:
                # ⚡ Bolt: talib.AD is the standard optimized C-implementation
                df["ad_line"] = talib.AD(high_vals, low_vals, close_vals, volume_vals)

            return df

        except Exception as e:
            logger.error(f"Error adding volume indicators: {e}")
            return df

    def add_trend_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add trend-based indicators"""
        try:
            # ⚡ Bolt: Extract raw values for TA-Lib
            high_vals = df["high"].values.astype(np.float64)
            low_vals = df["low"].values.astype(np.float64)
            close_vals = df["close"].values.astype(np.float64)

            # Parabolic SAR (Optimized: TA-Lib)
            if len(df) >= 5:
                # ⚡ Bolt: Using talib.SAR is much faster than the iterative loop
                df["sar"] = talib.SAR(
                    high_vals, low_vals, acceleration=0.02, maximum=0.2
                )

            # Average Directional Index (ADX) (Optimized: TA-Lib)
            if len(df) >= 14:
                # ⚡ Bolt: talib.ADX is standard and highly optimized
                df["adx"] = talib.ADX(high_vals, low_vals, close_vals, timeperiod=14)
                # Plus/Minus Directional Indicators
                df["di_plus"] = talib.PLUS_DI(
                    high_vals, low_vals, close_vals, timeperiod=14
                )
                df["di_minus"] = talib.MINUS_DI(
                    high_vals, low_vals, close_vals, timeperiod=14
                )

            # Aroon Indicator (Optimized: TA-Lib)
            if len(df) >= 25:
                # ⚡ Bolt: Using talib.AROON is significantly faster than sliding_window_view
                aroon_down, aroon_up = talib.AROON(high_vals, low_vals, timeperiod=25)
                df["aroon_up"] = aroon_up
                df["aroon_down"] = aroon_down
                df["aroon_oscillator"] = aroon_up - aroon_down

            # Trend strength (Optimized: TA-Lib Linear Regression Slope)
            periods = [10, 20, 50]
            for period in periods:
                if len(df) >= period:
                    # ⚡ Bolt: talib.LINEARREG_SLOPE provides a massive speedup
                    df[f"trend_strength_{period}"] = talib.LINEARREG_SLOPE(
                        close_vals, timeperiod=period
                    )

            return df

        except Exception as e:
            logger.error(f"Error adding trend indicators: {e}")
            return df

    def add_support_resistance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add support and resistance levels"""
        try:
            # Pivot Points
            if len(df) >= 1:
                # ⚡ Bolt: Extract raw values
                high_vals = df["high"].values.astype(np.float64)
                low_vals = df["low"].values.astype(np.float64)
                close_vals = df["close"].values.astype(np.float64)

                pivot = (
                    df["typical_price"].values
                    if "typical_price" in df.columns
                    else (high_vals + low_vals + close_vals) / 3
                )

                df["pivot"] = pivot
                df["r1"] = 2 * pivot - low_vals
                df["s1"] = 2 * pivot - high_vals
                df["r2"] = pivot + (high_vals - low_vals)
                df["s2"] = pivot - (high_vals - low_vals)

            # Price position relative to recent highs/lows (Optimized: TA-Lib)
            periods = [20, 50]
            for period in periods:
                if len(df) >= period:
                    # ⚡ Bolt: Using talib.MIN/MAX is faster than sliding_window_view
                    high_max_vals = talib.MAX(
                        df["high"].values.astype(np.float64), timeperiod=period
                    )
                    low_min_vals = talib.MIN(
                        df["low"].values.astype(np.float64), timeperiod=period
                    )

                    # ---
                    # ⚡ Bolt Optimization: Use raw numpy values for position arithmetic
                    # ---
                    close_vals = df["close"].values.astype(np.float64)
                    range_val = high_max_vals - low_min_vals

                    df[f"price_position_{period}"] = (
                        close_vals - low_min_vals
                    ) / range_val
                    df[f"resistance_distance_{period}"] = (
                        high_max_vals - close_vals
                    ) / close_vals
                    df[f"support_distance_{period}"] = (
                        close_vals - low_min_vals
                    ) / close_vals

            return df

        except Exception as e:
            logger.error(f"Error adding support/resistance indicators: {e}")
            return df

    def get_indicator_summary(self, df: pd.DataFrame) -> Dict:
        """Get summary of current indicator values"""
        try:
            if len(df) == 0:
                return {}

            latest = df.iloc[-1]
            summary = {}

            # Trend indicators
            if "sma_20" in df.columns and "sma_50" in df.columns:
                summary["trend"] = (
                    "UPTREND" if latest["sma_20"] > latest["sma_50"] else "DOWNTREND"
                )

            # Momentum
            if "rsi" in df.columns:
                rsi = latest["rsi"]
                if rsi > 70:
                    summary["momentum"] = "OVERBOUGHT"
                elif rsi < 30:
                    summary["momentum"] = "OVERSOLD"
                else:
                    summary["momentum"] = "NEUTRAL"

            # Volatility
            if "atr" in df.columns:
                current_atr = latest["atr"]
                avg_atr = df["atr"].tail(20).mean()
                summary["volatility"] = (
                    "HIGH" if current_atr > avg_atr * 1.5 else "NORMAL"
                )

            # Bollinger Bands position
            if "bb_position" in df.columns:
                bb_pos = latest["bb_position"]
                if bb_pos > 0.8:
                    summary["bb_position"] = "UPPER"
                elif bb_pos < 0.2:
                    summary["bb_position"] = "LOWER"
                else:
                    summary["bb_position"] = "MIDDLE"

            return summary

        except Exception as e:
            logger.error(f"Error getting indicator summary: {e}")
            return {}
