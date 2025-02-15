from smartapi import SmartConnect
from typing import Dict, Any
import os
from datetime import datetime

class OrderManager:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.smart_api = SmartConnect(api_key=self.api_key)

    async def place_order(self, order_params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            order = {
                "variety": "NORMAL",
                "tradingsymbol": order_params["symbol"],
                "symboltoken": order_params["token"],
                "transactiontype": order_params["transaction_type"],
                "exchange": "NSE",
                "ordertype": order_params["order_type"],
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": order_params["price"],
                "quantity": order_params["quantity"]
            }
            
            order_id = self.smart_api.placeOrder(order)
            return {"status": "success", "order_id": order_id}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def modify_order(self, order_id: str, modifications: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.smart_api.modifyOrder(
                order_id=order_id,
                price=modifications.get("price"),
                quantity=modifications.get("quantity"),
                ordertype=modifications.get("order_type", "LIMIT")
            )
            return {"status": "success", "response": response}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        try:
            response = self.smart_api.cancelOrder(order_id=order_id)
            return {"status": "success", "response": response}
        except Exception as e:
            return {"status": "error", "message": str(e)}
