import os
from dotenv import load_dotenv
import requests

from services.uniswap import get_pool_data

COINSTORE_API_URL = "https://api.coinstore.com/api/v1/ticker/price"
BITMART_API_URL = "https://api-cloud.bitmart.com/spot/v1/ticker"
load_dotenv()

COINSTORE_API_KEY = os.environ.get("COINSTORE_API_KEY")
BITMART_API_KEY = os.environ.get("BITMART_API_KEY")

coinstore_headers = {
    "accept": "application/json",
}
if COINSTORE_API_KEY:
    coinstore_headers["X-API-KEY"] = COINSTORE_API_KEY

bitmart_headers = {
    "accept": "application/json",
}
if BITMART_API_KEY:
    bitmart_headers["X-BM-KEY"] = BITMART_API_KEY

def get_uniswap_price():
    try:
        data = get_pool_data()
        return round(data["price"], 6)
    except Exception as e:
        print("Uniswap price fetch error:", e)
        return None

def get_coinstore_price():
    try:
        response = requests.get(
            COINSTORE_API_URL,
            headers=coinstore_headers,
            params={"symbol": "SHARPUSDT"}
        )
        data = response.json()
        if data.get("data") and isinstance(data["data"], list):
            for token in data["data"]:
                if token.get("symbol") == "SHARPUSDT" and token.get("price") is not None:
                    return float(token["price"])
    except Exception as e:
        print("Coinstore API fetch error:", e)
    return None

def get_bitmart_price():
    try:
        response = requests.get(BITMART_API_URL, headers=bitmart_headers)
        data = response.json()
        tickers = data.get("data", {}).get("tickers", [])
        for ticker in tickers:
            if ticker.get("symbol") == "SHARP_USDT" and ticker.get("last_price") is not None:
                return float(ticker["last_price"])
    except Exception as e:
        print("BitMart API fetch error:", e)
    return None

def main():
    coinstore_price = get_coinstore_price()
    bitmart_price = get_bitmart_price()
    uniswap_price = get_uniswap_price()

    print("\nCurrent SHARP/USDT Prices:")
    print("Coinstore:", coinstore_price if coinstore_price else "Unavailable")
    print("BitMart:", bitmart_price if bitmart_price else "Unavailable")
    print("Uniswap:", uniswap_price if uniswap_price else "Unavailable")

if __name__ == "__main__":
    main()
