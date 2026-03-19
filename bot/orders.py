from typing import Any, Dict, Optional
import math
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

def place_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> Dict[str, Any]:
    try:
        # 1. Sabse pehle Leverage set karein (Insufficient Margin fix karne ke liye)
        client.futures_change_leverage(symbol=symbol, leverage=10)
        
        # 2. Minimum Notional Check (100 USDT requirement fix karne ke liye)
        ticker = client.futures_symbol_ticker(symbol=symbol)
        curr_price = float(ticker['price'])
        
        # Agar LIMIT order hai toh user ka price use karein, varna MARKET price
        check_price = price if (order_type == "LIMIT" and price) else curr_price
        
        # Check karein ki kya (Qty * Price) < 100 hai?
        if (quantity * check_price) < 100:
            # Nayi quantity calculate karein jo 105 USDT ki ho (safety ke liye)
            quantity = round(105 / check_price, 3)
            print(f"[*] Adjusted quantity to {quantity} to meet 100 USDT minimum requirement.")

        # 3. Order parameters tyar karein
        order_params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }

        if order_type.upper() == "MARKET":
            response = client.futures_create_order(**order_params)

        elif order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT order")
            
            order_params.update({
                "price": price,
                "timeInForce": "GTC"
            })
            response = client.futures_create_order(**order_params)

        else:
            raise ValueError("Unsupported order type")

        return {
            "success": True,
            "data": response,
            "message": "Order placed successfully"
        }

    except (BinanceAPIException, BinanceOrderException) as exc:
        return {
            "success": False,
            "data": None,
            "message": f"Binance error: {str(exc)}"
        }
    except Exception as exc:
        return {
            "success": False,
            "data": None,
            "message": f"Unexpected error: {str(exc)}"
        }


def extract_order_summary(response: Dict[str, Any]) -> Dict[str, Any]:
    # Agar error response hai toh usko handle karein
    if not response.get("success"):
        return {
            "status": "FAILED",
            "message": response.get("message", "Unknown error")
        }

    order = response.get("data", {})
    if not order:
        return {"status": "FAILED", "message": "No data received"}

    return {
        "orderId": order.get("orderId"),
        "symbol": order.get("symbol"),
        "status": order.get("status"),
        "side": order.get("side"),
        "type": order.get("type"),
        "executedQty": order.get("executedQty"),
        "avgPrice": order.get("avgPrice", "0.0"),
        "price": order.get("price"),
        "message": response.get("message"),
    }