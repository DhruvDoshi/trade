from smartapi import SmartConnect
import pandas as pd
from typing import Dict, List, Optional
import logging

class MarketQuotes:
    def __init__(self, api: SmartConnect):
        self.api = api
        self.logger = logging.getLogger(__name__)

    def get_ltp(self, tokens: List[str]) -> Dict[str, float]:
        """Get Last Traded Price for given tokens"""
        try:
            response = {}
            for token in tokens:
                data = self.api.ltpData("NSE", token, "EQ")
                if data.get("data"):
                    response[token] = data["data"]["ltp"]
            return response
        except Exception as e:
            self.logger.error(f"Error fetching LTP: {str(e)}")
            return {}

    def get_quote(self, token: str) -> Optional[Dict]:
        """Get detailed quote for a symbol"""
        try:
            return self.api.getQuote("NSE", token, "EQ")
        except Exception as e:
            self.logger.error(f"Error fetching quote: {str(e)}")
            return None

    def get_historical(self, token: str, interval: str, from_date: str, to_date: str) -> pd.DataFrame:
        """Get historical data for analysis"""
        try:
            data = self.api.getCandleData({
                "exchange": "NSE",
                "symboltoken": token,
                "interval": interval,
                "fromdate": from_date,
                "todate": to_date
            })
            return pd.DataFrame(data)
        except Exception as e:
            self.logger.error(f"Error fetching historical data: {str(e)}")
            return pd.DataFrame()
