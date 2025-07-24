import requests
import re

BITMART_URL = "https://www.bitmart.com/trade/en-US?type=spot&symbol=SHARP_USDT"
COINSTORE_URL = "https://www.coinstore.com/spot/SHARPUSDT"


def fetch_bitmart_price():
    resp = requests.get(BITMART_URL, timeout=10)
    m = re.search(r'"lastPrice":"([0-9.]+)"', resp.text)
    if not m:
        return None
    return float(m.group(1))


def fetch_coinstore_price():
    resp = requests.get(COINSTORE_URL, timeout=10)
    m = re.search(r'"last":"([0-9.]+)"', resp.text)
    if not m:
        return None
    return float(m.group(1))


def get_average_price():
    bm = fetch_bitmart_price()
    cs = fetch_coinstore_price()
    prices = [p for p in [bm, cs] if p is not None]
    if not prices:
        return None, bm, cs
    return sum(prices) / len(prices), bm, cs
