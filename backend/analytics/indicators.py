import numpy as np
import pandas as pd
from typing import List, Dict

class TechnicalIndicators:
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> List[float]:
        return list(pd.Series(prices).rolling(window=period).mean())

    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
        delta = pd.Series(prices).diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return list(100 - (100 / (1 + rs)))

    @staticmethod
    def calculate_macd(prices: List[float]) -> Dict[str, List[float]]:
        price_series = pd.Series(prices)
        exp1 = price_series.ewm(span=12, adjust=False).mean()
        exp2 = price_series.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        
        return {
            "macd": list(macd),
            "signal": list(signal),
            "histogram": list(macd - signal)
        }
