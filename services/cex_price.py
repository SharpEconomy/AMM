"""Helpers for fetching SHARP/USDT prices from centralized exchanges."""

from __future__ import annotations
import json
import requests

BITMART_API_URL = "https://api-cloud.bitmart.com/spot/quotation/v3/tickers?symbol=SHARP_USDT"
COINSTORE_API_URL = "https://api.coinstore.com/api/v1/ticker/price"
coinstore_headers = {
    "accept": "application/json",
    "X-API-KEY": "cc5025cfef8568b17256a6dabaa96b41"
}

bitmart_headers = {
    "accept": "application/json",
    "X-BM-KEY": "e19759833776964c26b3b906e04bf9e7a22c55e9"
}

def fetch_bitmart_price():
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

def fetch_coinstore_price():
    """Return the latest Coinstore price or ``None`` on failure."""
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
