from smartapi import SmartConnect
from typing import Dict, Any, Optional
import logging
from datetime import datetime

class OrderManager:
    def __init__(self, api: SmartConnect):
        self.api = api
        self.logger = logging.getLogger(__name__)

    def place_order(self, 
                   symbol: str,
                   token: str,
                   qty: int,
                   side: str,
                   order_type: str = "MARKET",
                   price: float = 0) -> Dict[str, Any]:
        """Place new order"""
        try:
            order_params = {
                "variety": "NORMAL",
                "tradingsymbol": symbol,
                "symboltoken": token,
                "transactiontype": side,
                "exchange": "NSE",
                "ordertype": order_type,
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": price,
                "quantity": qty
            }
            
            order_id = self.api.placeOrder(order_params)
            return {
                "status": "success",
                "order_id": order_id,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Order placement failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def place_bracket_order(self,
                          symbol: str,
                          token: str,
                          qty: int,
                          side: str,
                          stoploss: float,
                          target: float,
                          price: float) -> Dict[str, Any]:
        """Place bracket order with SL and target"""
        try:
            order_params = {
                "variety": "BO",
                "tradingsymbol": symbol,
                "symboltoken": token,
                "transactiontype": side,
                "exchange": "NSE",
                "ordertype": "LIMIT",
                "producttype": "BO",
                "duration": "DAY",
                "price": price,
                "quantity": qty,
                "squareoff": abs(target - price),
                "stoploss": abs(stoploss - price)
            }
            
            order_id = self.api.placeOrder(order_params)
            return {
                "status": "success",
                "order_id": order_id,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Bracket order placement failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def modify_order(self,
                    order_id: str,
                    new_qty: Optional[int] = None,
                    new_price: Optional[float] = None) -> Dict[str, Any]:
        """Modify existing order"""
        try:
            response = self.api.modifyOrder(
                order_id=order_id,
                price=new_price,
                quantity=new_qty,
                ordertype="LIMIT"
            )
            return {"status": "success", "response": response}
        except Exception as e:
            self.logger.error(f"Order modification failed: {str(e)}")
            return {"status": "error", "message": str(e)}
