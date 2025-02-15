import pandas as pd
import numpy as np
from typing import Dict, List, Union
import logging

class PriceAnalysis:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_support_resistance(self, data: pd.DataFrame, periods: int = 20) -> Dict[str, float]:
        """Calculate support and resistance levels"""
        try:
            high = data['high'].rolling(window=periods).max()
            low = data['low'].rolling(window=periods).min()
            
            return {
                "support": float(low.iloc[-1]),
                "resistance": float(high.iloc[-1])
            }
        except Exception as e:
            self.logger.error(f"Error calculating support/resistance: {str(e)}")
            return {"support": 0, "resistance": 0}

    def get_trend(self, prices: List[float], period: int = 14) -> str:
        """Determine trend direction"""
        try:
            df = pd.DataFrame(prices, columns=['price'])
            sma = df['price'].rolling(window=period).mean()
            current_price = prices[-1]
            
            if current_price > sma.iloc[-1]:
                return "UPTREND"
            elif current_price < sma.iloc[-1]:
                return "DOWNTREND"
            return "SIDEWAYS"
        except Exception as e:
            self.logger.error(f"Error determining trend: {str(e)}")
            return "UNKNOWN"

    def detect_breakout(self, 
                       data: pd.DataFrame, 
                       resistance: float, 
                       support: float, 
                       threshold: float = 0.02) -> str:
        """Detect breakout signals"""
        try:
            current_price = data['close'].iloc[-1]
            
            if current_price > resistance * (1 + threshold):
                return "BREAKOUT_UP"
            elif current_price < support * (1 - threshold):
                return "BREAKOUT_DOWN"
            return "NO_BREAKOUT"
        except Exception as e:
            self.logger.error(f"Error detecting breakout: {str(e)}")
            return "ERROR"
