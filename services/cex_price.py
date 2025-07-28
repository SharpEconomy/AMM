"""Helpers for fetching SHARP/USDT prices from centralized exchanges."""

from __future__ import annotations

import json
import logging
from typing import Optional, Tuple

import requests

BITMART_URL = "https://api-cloud.bitmart.com/spot/quotation/v3/tickers?symbol=SHARP_USDT"
COINSTORE_URL = "https://api.coinstore.com/api/v1/ticker?symbol=SHARPUSDT"


def _safe_request(url: str) -> Optional[str]:
    """Return response text or ``None`` and log failures."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as exc:  # pragma: no cover - network
        logging.warning("Request failed for %s: %s", url, exc)
        return None

def fetch_bitmart_price() -> Optional[float]:
    """Return the latest Bitmart price or ``None`` on failure."""
    text = _safe_request(BITMART_URL)
    if not text:
        return None
    try:
        data = json.loads(text)
        tickers = data.get("data")
        if isinstance(tickers, dict):
            tickers = tickers.get("tickers")

        if isinstance(tickers, list):
            for t in tickers:
                # Handle both dict and list formats returned by the API
                if isinstance(t, dict):
                    if t.get("symbol") == "SHARP_USDT" and t.get("last_price") is not None:
                        return float(t["last_price"])
                elif isinstance(t, list) and len(t) >= 2 and t[0] == "SHARP_USDT":
                    return float(t[1])
    except (ValueError, json.JSONDecodeError, TypeError) as exc:
        logging.warning("Failed to parse Bitmart response: %s", exc)
    return None

def fetch_coinstore_price() -> Optional[float]:
    """Return the latest Coinstore price or ``None`` on failure."""
    text = _safe_request(COINSTORE_URL)
    if not text:
        return None
    try:
        data = json.loads(text)
        price = None
        if isinstance(data, dict):
            inner = data.get("data")
            if isinstance(inner, dict) and "last" in inner:
                price = inner["last"]
        if price is not None:
            return float(price)
    except (ValueError, json.JSONDecodeError, TypeError) as exc:
        logging.warning("Failed to parse Coinstore response: %s", exc)
    return None


def get_average_price() -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """Return the average price along with individual exchange prices."""
    bm = fetch_bitmart_price()
    cs = fetch_coinstore_price()
    prices = [p for p in (bm, cs) if p is not None]
    if not prices:
        return None, bm, cs
    return sum(prices) / len(prices), bm, cs

