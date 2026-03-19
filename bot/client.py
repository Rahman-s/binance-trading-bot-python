import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

TESTNET_BASE_URL = "https://testnet.binancefuture.com/fapi"

def get_binance_client() -> Client:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("Missing API credentials in .env file")

    client = Client(api_key, api_secret, testnet=True)
    

    client.FUTURES_URL = TESTNET_BASE_URL
    
    return client

def setup_account(client: Client, symbol: str):
    """
    Ye function margin aur leverage set karega taaki error na aaye.
    """
    try:
        client.futures_change_margin_type(symbol=symbol, marginType='CROSS')
    except Exception as e:
        pass

    client.futures_change_leverage(symbol=symbol, leverage=10)
    print(f"Account setup for {symbol}: Leverage set to 10x, Margin: CROSS")