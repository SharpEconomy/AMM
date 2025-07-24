"""Helpers for fetching CEX prices."""

import json
from typing import Optional, Tuple

import requests

BITMART_URL = "https://api-cloud.bitmart.com/spot/quotation/v3/tickers?symbol=SHARP_USDT"
COINSTORE_URL = "https://api.coinstore.com/api/v1/ticker?symbol=SHARPUSDT"

def _safe_request(url: str) -> Optional[str]:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException:
        return None


def fetch_bitmart_price() -> Optional[float]:
    """Return the latest Bitmart price or ``None`` on failure."""
    text = _safe_request(BITMART_URL)
    if not text:
        return None
    try:
        data = json.loads(text)
        ticker = data["data"]["tickers"][0]
        return float(ticker["last_price"])
    except (KeyError, ValueError, IndexError, json.JSONDecodeError):
        return None

def fetch_coinstore_price() -> Optional[float]:
    """Return the latest Coinstore price or ``None`` on failure."""
    text = _safe_request(COINSTORE_URL)
    if not text:
      return None
    try:
        data = json.loads(text)
        return float(data["data"]["last"])
    except (KeyError, ValueError, json.JSONDecodeError):
        return None


def get_average_price() -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """Return the average price along with individual exchange prices."""
    bm = fetch_bitmart_price()
    cs = fetch_coinstore_price()
    prices = [p for p in (bm, cs) if p is not None]
    if not prices:
        return None, bm, cs
    return sum(prices) / len(prices), bm, cs
