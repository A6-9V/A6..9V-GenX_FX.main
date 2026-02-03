import os

import joblib
import numpy as np
import pandas as pd
import talib
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class FeatureEngineer:
    """
    Handles all feature engineering tasks, including indicator calculation,
    pattern detection, and data scaling.
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.price_scaler = MinMaxScaler()

    def engineer_features(self, df: pd.DataFrame, sequence_length: int):
        """Engineers features for training the ensemble models."""

        indicators = self._calculate_technical_indicators(df)
        patterns = self._detect_chart_patterns(df)

        features = np.hstack([indicators, patterns])
        features = self.scaler.fit_transform(features)

        price_sequences = self._create_price_sequences(df, sequence_length)
        chart_patterns = self._create_chart_images(df, sequence_length)

        labels = self._generate_labels(df)

        # Align all data to the same length
        min_len = min(
            len(features), len(price_sequences), len(chart_patterns), len(labels)
        )

        return self.FeatureSet(
            technical_indicators=features[-min_len:],
            price_sequences=price_sequences[-min_len:],
            chart_patterns=chart_patterns[-min_len:],
            labels=labels[-min_len:],
        )

    def engineer_features_for_prediction(self, df: pd.DataFrame, sequence_length: int):
        """
        Engineers features for a single prediction.
        ⚡ Bolt Optimization: Uses only_last=True to skip redundant historical calculations.
        """
        indicators = self._calculate_technical_indicators(df)
        patterns = self._detect_chart_patterns(df)

        features = np.hstack([indicators, patterns])
        features = self.scaler.transform(features)

        # Optimization: Only calculate the last sequence/image needed for prediction
        price_sequences = self._create_price_sequences(
            df, sequence_length, only_last=True
        )
        chart_patterns = self._create_chart_images(df, sequence_length, only_last=True)

        return self.FeatureSet(
            technical_indicators=features[-1:],
            price_sequences=price_sequences,
            chart_patterns=chart_patterns,
            labels=None,
        )

    def _calculate_technical_indicators(self, df: pd.DataFrame) -> np.ndarray:
        """Calculate comprehensive technical indicators"""
        features = []

        # Price-based features
        features.extend(
            [
                df["close"].pct_change(),  # Returns
                df["high"] / df["close"] - 1,  # High-Close ratio
                df["low"] / df["close"] - 1,  # Low-Close ratio
                df["volume"].pct_change(),  # Volume change
            ]
        )

        # Moving averages
        for period in [5, 10, 20, 50, 100]:
            ma = df["close"].rolling(period).mean()
            features.append(df["close"] / ma - 1)  # Price relative to MA

        # Technical indicators using TA-Lib
        features.extend(
            [
                talib.RSI(df["close"], timeperiod=14) / 100,  # Normalized RSI
                talib.MACD(df["close"])[0],  # MACD line
                talib.MACD(df["close"])[1],  # MACD signal
                talib.MACD(df["close"])[2],  # MACD histogram
                talib.BBANDS(df["close"])[0],  # Bollinger Upper
                talib.BBANDS(df["close"])[1],  # Bollinger Middle
                talib.BBANDS(df["close"])[2],  # Bollinger Lower
                talib.ATR(df["high"], df["low"], df["close"]),  # ATR
                talib.CCI(df["high"], df["low"], df["close"]),  # CCI
                talib.WILLR(df["high"], df["low"], df["close"]),  # Williams %R
                talib.ADX(df["high"], df["low"], df["close"]),  # ADX
                talib.MOM(df["close"]),  # Momentum
                talib.ROC(df["close"]),  # Rate of Change
            ]
        )

        # Stochastic Oscillator
        stoch_k, stoch_d = talib.STOCH(df["high"], df["low"], df["close"])
        features.extend([stoch_k, stoch_d])

        # Volume indicators
        features.extend(
            [
                talib.OBV(df["close"], df["volume"]),
                talib.AD(df["high"], df["low"], df["close"], df["volume"]),
            ]
        )

        # Combine all features
        feature_matrix = np.column_stack(features)

        # Handle NaN values
        feature_matrix = np.nan_to_num(feature_matrix, nan=0.0, posinf=0.0, neginf=0.0)

        return feature_matrix

    def _detect_chart_patterns(self, df: pd.DataFrame) -> np.ndarray:
        """Detect candlestick and chart patterns"""
        patterns = []

        # Candlestick patterns using TA-Lib
        pattern_functions = [
            talib.CDL2CROWS,
            talib.CDL3BLACKCROWS,
            talib.CDL3INSIDE,
            talib.CDL3LINESTRIKE,
            talib.CDL3OUTSIDE,
            talib.CDL3STARSINSOUTH,
            talib.CDL3WHITESOLDIERS,
            talib.CDLABANDONEDBABY,
            talib.CDLADVANCEBLOCK,
            talib.CDLBELTHOLD,
            talib.CDLBREAKAWAY,
            talib.CDLCLOSINGMARUBOZU,
            talib.CDLCONCEALBABYSWALL,
            talib.CDLCOUNTERATTACK,
            talib.CDLDARKCLOUDCOVER,
            talib.CDLDOJI,
            talib.CDLDOJISTAR,
            talib.CDLDRAGONFLYDOJI,
            talib.CDLENGULFING,
            talib.CDLEVENINGDOJISTAR,
            talib.CDLEVENINGSTAR,
            talib.CDLGAPSIDESIDEWHITE,
            talib.CDLGRAVESTONEDOJI,
            talib.CDLHAMMER,
            talib.CDLHANGINGMAN,
            talib.CDLHARAMI,
            talib.CDLHARAMICROSS,
            talib.CDLHIGHWAVE,
            talib.CDLHIKKAKE,
            talib.CDLHOMINGPIGEON,
            talib.CDLIDENTICAL3CROWS,
            talib.CDLINNECK,
            talib.CDLINVERTEDHAMMER,
            talib.CDLKICKING,
            talib.CDLKICKINGBYLENGTH,
            talib.CDLLADDERBOTTOM,
            talib.CDLLONGLEGGEDDOJI,
            talib.CDLLONGLINE,
            talib.CDLMARUBOZU,
            talib.CDLMATCHINGLOW,
            talib.CDLMATHOLD,
            talib.CDLMORNINGDOJISTAR,
            talib.CDLMORNINGSTAR,
            talib.CDLONNECK,
            talib.CDLPIERCING,
            talib.CDLRICKSHAWMAN,
            talib.CDLRISEFALL3METHODS,
            talib.CDLSEPARATINGLINES,
            talib.CDLSHOOTINGSTAR,
            talib.CDLSHORTLINE,
            talib.CDLSPINNINGTOP,
            talib.CDLSTALLEDPATTERN,
            talib.CDLSTICKSANDWICH,
            talib.CDLTAKURI,
            talib.CDLTASUKIGAP,
            talib.CDLTHRUSTING,
            talib.CDLTRISTAR,
            talib.CDLUNIQUE3RIVER,
            talib.CDLUPSIDEGAP2CROWS,
            talib.CDLXSIDEGAP3METHODS,
        ]

        for pattern_func in pattern_functions:
            try:
                pattern = pattern_func(df["open"], df["high"], df["low"], df["close"])
                patterns.append(pattern)
            except Exception:
                # Some patterns might fail, add zeros
                patterns.append(np.zeros(len(df)))

        # Combine all patterns
        pattern_matrix = np.column_stack(patterns)

        # Normalize patterns (-1, 0, 1) to (0, 0.5, 1)
        pattern_matrix = (pattern_matrix + 1) / 2

        return pattern_matrix

    def _create_price_sequences(
        self, df: pd.DataFrame, sequence_length: int, only_last: bool = False
    ) -> np.ndarray:
        """
        Creates sequences of price data for LSTMs.
        ⚡ Bolt Optimization: Vectorized using sliding_window_view and added only_last for inference.
        """
        price_data = df[["open", "high", "low", "close", "volume"]].values
        scaled_data = self.price_scaler.fit_transform(price_data)

        if only_last:
            # For a single prediction, we only need the most recent sequence.
            # This avoids expensive windowing over the entire history.
            return np.array([scaled_data[-sequence_length:]])

        # Vectorized windowing using numpy stride tricks
        # Shape: (N-W+1, W, 5)
        return np.lib.stride_tricks.sliding_window_view(
            scaled_data, window_shape=sequence_length, axis=0
        ).transpose(0, 2, 1)

    def _create_chart_images(
        self, df: pd.DataFrame, sequence_length: int, only_last: bool = False
    ) -> np.ndarray:
        """
        Create chart-like images for CNN model
        ⚡ Bolt Optimization: Vectorized using sliding_window_view and added only_last for inference.
        """
        # Calculate indicators for imaging once
        rsi = talib.RSI(df["close"], timeperiod=14).fillna(0.5).values
        macd_line, _, macd_hist = talib.MACD(df["close"])
        macd_line = macd_line.fillna(0).values
        macd_hist = macd_hist.fillna(0).values
        close = df["close"].values

        if only_last:
            # Matches original buggy behavior where the very last element of df was excluded.
            # Original: range(W, len(df)) -> last i is len(df)-1 -> window is len(df)-1-W : len(df)-1
            window_close = close[-1 - sequence_length : -1]
            window_rsi = rsi[-1 - sequence_length : -1]
            window_macd_line = macd_line[-1 - sequence_length : -1]
            window_macd_hist = macd_hist[-1 - sequence_length : -1]

            price_norm = (window_close - np.min(window_close)) / (
                np.max(window_close) - np.min(window_close) + 1e-8
            )

            image = np.column_stack(
                [price_norm, window_rsi, window_macd_line, window_macd_hist]
            )
            return np.array([image])

        # Vectorized implementation for training/bulk processing
        # Note: We take [:-1] to exactly match the original iterative behavior which
        # excluded the latest price point in the chart images.
        close_windows = np.lib.stride_tricks.sliding_window_view(
            close, window_shape=sequence_length
        )[:-1]
        rsi_windows = np.lib.stride_tricks.sliding_window_view(
            rsi, window_shape=sequence_length
        )[:-1]
        macd_line_windows = np.lib.stride_tricks.sliding_window_view(
            macd_line, window_shape=sequence_length
        )[:-1]
        macd_hist_windows = np.lib.stride_tricks.sliding_window_view(
            macd_hist, window_shape=sequence_length
        )[:-1]

        # Vectorized normalization
        mins = np.min(close_windows, axis=1, keepdims=True)
        maxs = np.max(close_windows, axis=1, keepdims=True)
        price_norm = (close_windows - mins) / (maxs - mins + 1e-8)

        # Stack channels to create (N-W, W, 4) structure
        return np.stack(
            [price_norm, rsi_windows, macd_line_windows, macd_hist_windows], axis=-1
        )

    def _generate_labels(
        self, df: pd.DataFrame, future_horizon=10, threshold=0.001
    ) -> np.ndarray:
        """Generates labels for training."""
        future_price = df["close"].shift(-future_horizon)
        price_change = (future_price - df["close"]) / df["close"]

        labels = np.ones(len(df), dtype=int)  # Hold
        labels[price_change > threshold] = 2  # Buy
        labels[price_change < -threshold] = 0  # Sell

        return labels

    def save_scalers(self, model_dir: str):
        """Saves the scalers to disk."""
        joblib.dump(self.scaler, os.path.join(model_dir, "feature_scaler.pkl"))
        joblib.dump(self.price_scaler, os.path.join(model_dir, "price_scaler.pkl"))

    def load_scalers(self, model_dir: str):
        """Loads the scalers from disk."""
        self.scaler = joblib.load(os.path.join(model_dir, "feature_scaler.pkl"))
        self.price_scaler = joblib.load(os.path.join(model_dir, "price_scaler.pkl"))

    class FeatureSet:
        """A simple container for the different types of features."""

        def __init__(
            self, technical_indicators, price_sequences, chart_patterns, labels
        ):
            self.technical_indicators = technical_indicators
            self.price_sequences = price_sequences
            self.chart_patterns = chart_patterns
            self.labels = labels
