def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol or len(symbol) < 6:
        raise ValueError("Symbol must look like BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in {"BUY", "SELL"}:
        raise ValueError("Side must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in {"MARKET", "LIMIT"}:
        raise ValueError("Order type must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
    except ValueError as exc:
        raise ValueError("Quantity must be a valid number") from exc

    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")
    return qty


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except ValueError as exc:
        raise ValueError("Price must be a valid number") from exc

    if p <= 0:
        raise ValueError("Price must be greater than 0")
    return p