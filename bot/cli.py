from pprint import pprint

from bot.client import get_binance_client
from bot.logging_config import setup_logger
from bot.orders import extract_order_summary, place_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

logger = setup_logger()


def print_header() -> None:
    print("\n" + "=" * 65)
    print("     Binance Futures Testnet - Simplified Trading Bot")
    print("=" * 65)


def ask_input(prompt_text: str) -> str:
    return input(f"{prompt_text}: ").strip()


def get_user_input():
    while True:
        try:
            symbol = validate_symbol(ask_input("Enter symbol (e.g. BTCUSDT)").upper())
            break
        except ValueError as exc:
            print(f"Invalid input -> {exc}")

    while True:
        try:
            side = validate_side(ask_input("Enter side (BUY/SELL)").upper())
            break
        except ValueError as exc:
            print(f"Invalid input -> {exc}")

    while True:
        try:
            order_type = validate_order_type(
                ask_input("Enter order type (MARKET/LIMIT)").upper()
            )
            break
        except ValueError as exc:
            print(f"Invalid input -> {exc}")

    while True:
        try:
            quantity = validate_quantity(ask_input("Enter quantity"))
            break
        except ValueError as exc:
            print(f"Invalid input -> {exc}")

    price = None
    if order_type == "LIMIT":
        while True:
            try:
                price = validate_price(ask_input("Enter price for LIMIT order"))
                break
            except ValueError as exc:
                print(f"Invalid input -> {exc}")

    return symbol, side, order_type, quantity, price


def print_order_request(symbol, side, order_type, quantity, price=None):
    print("\nOrder Request Summary")
    print("-" * 30)
    print(f"Symbol     : {symbol}")
    print(f"Side       : {side}")
    print(f"Order Type : {order_type}")
    print(f"Quantity   : {quantity}")
    if price is not None:
        print(f"Price      : {price}")


def confirm_order() -> bool:
    while True:
        choice = ask_input("Do you want to place this order? (yes/no)").lower()
        if choice in {"yes", "y"}:
            return True
        if choice in {"no", "n"}:
            return False
        print("Please enter yes or no.")


def print_result(summary: dict, success: bool):
    print("\nOrder Response Summary")
    print("-" * 30)
    pprint(summary)

    if success:
        print("\nStatus: SUCCESS")
    else:
        print("\nStatus: FAILED")


def main():
    try:
        print_header()
        client = get_binance_client()

        symbol, side, order_type, quantity, price = get_user_input()

        print_order_request(symbol, side, order_type, quantity, price)

        if not confirm_order():
            print("\nOrder cancelled by user.")
            logger.info("Order cancelled by user before API call")
            return

        logger.info(
            "Order Request | symbol=%s side=%s type=%s quantity=%s price=%s",
            symbol, side, order_type, quantity, price
        )

        response = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        logger.info("Raw API Response | %s", response)

        summary = extract_order_summary(response)
        print_result(summary, response["success"])

        if response["success"]:
            logger.info("Success | %s", summary)
        else:
            logger.error("Failure | %s", response["message"])

    except Exception as exc:
        logger.exception("Unhandled Exception")
        print(f"\nUnexpected Error: {exc}")


if __name__ == "__main__":
    main()