from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from smartapi import SmartConnect
import os

from modules.quotes import MarketQuotes
from modules.analysis import PriceAnalysis
from modules.orders import OrderManager
from database.session import get_db

load_dotenv()

app = FastAPI(title="Trading Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize API client
api = SmartConnect(api_key=os.getenv("API_KEY"))
quotes = MarketQuotes(api)
analysis = PriceAnalysis()
orders = OrderManager(api)

@app.get("/")
async def root():
    return {"message": "Trading Application API"}

@app.post("/order/place")
async def place_order(order_params: Dict[str, Any], db: Session = Depends(get_db)):
    result = await orders.place_order(order_params)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/order/{order_id}/modify")
async def modify_order(order_id: str, modifications: Dict[str, Any], db: Session = Depends(get_db)):
    result = await orders.modify_order(order_id, modifications)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.delete("/order/{order_id}")
async def cancel_order(order_id: str, db: Session = Depends(get_db)):
    result = await orders.cancel_order(order_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/indicators/{symbol}")
async def get_indicators(symbol: str, db: Session = Depends(get_db)):
    # Fetch historical prices from database
    # This is a placeholder - implement actual data fetching
    prices = [100, 101, 99, 102, 98, 103]  # Example prices
    
    return {
        "sma": indicators.calculate_sma(prices, 5),
        "rsi": indicators.calculate_rsi(prices),
        "macd": indicators.calculate_macd(prices)
    }

@app.get("/quote/{symbol}")
async def get_quote(symbol: str):
    quote = quotes.get_quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote

@app.get("/analysis/{symbol}")
async def get_analysis(symbol: str):
    historical = quotes.get_historical(
        symbol,
        "ONE_MINUTE",
        "2024-01-01 09:15",
        "2024-01-01 15:30"
    )
    
    if historical.empty:
        raise HTTPException(status_code=404, detail="Historical data not found")
    
    support_resistance = analysis.calculate_support_resistance(historical)
    trend = analysis.get_trend(historical['close'].tolist())
    breakout = analysis.detect_breakout(
        historical,
        support_resistance['resistance'],
        support_resistance['support']
    )
    
    return {
        "trend": trend,
        "breakout": breakout,
        "levels": support_resistance
    }

@app.post("/order/bracket")
async def place_bracket_order(
    symbol: str,
    token: str,
    quantity: int,
    side: str,
    price: float,
    stoploss: float,
    target: float
):
    result = orders.place_bracket_order(
        symbol=symbol,
        token=token,
        qty=quantity,
        side=side,
        stoploss=stoploss,
        target=target,
        price=price
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result
