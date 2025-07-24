"""Helpers for fetching CEX prices."""

import re
from typing import Optional, Tuple

import requests

BITMART_URL = "https://www.bitmart.com/trade/en-US?type=spot&symbol=SHARP_USDT"
COINSTORE_URL = "https://www.coinstore.com/spot/SHARPUSDT"


_BITMART_RE = re.compile(r'"lastPrice":"([0-9.]+)"')
_COINSTORE_RE = re.compile(r'"last":"([0-9.]+)"')


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
    match = _BITMART_RE.search(text)
    return float(match.group(1)) if match else None


def fetch_coinstore_price() -> Optional[float]:
    """Return the latest Coinstore price or ``None`` on failure."""
    text = _safe_request(COINSTORE_URL)
    if not text:
        return None
    match = _COINSTORE_RE.search(text)
    return float(match.group(1)) if match else None


def get_average_price() -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """Return the average price along with individual exchange prices."""
    bm = fetch_bitmart_price()
    cs = fetch_coinstore_price()
    prices = [p for p in (bm, cs) if p is not None]
    if not prices:
        return None, bm, cs
    return sum(prices) / len(prices), bm, cs
