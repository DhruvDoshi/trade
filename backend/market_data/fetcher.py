from smartapi import SmartConnect
from typing import Dict, Any
import os

class MarketDataFetcher:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.client_id = os.getenv("CLIENT_ID")
        self.password = os.getenv("PASSWORD")
        self.smart_api = SmartConnect(api_key=self.api_key)

    async def connect(self) -> bool:
        try:
            data = self.smart_api.generateSession(self.client_id, self.password)
            return True if data['status'] else False
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    async def get_market_data(self, symbol: str) -> Dict[str, Any]:
        try:
            data = self.smart_api.ltpData("NSE", symbol, "EQ")
            return data
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return {}
