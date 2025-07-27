"""Utilities for reading Uniswap V3 pool data via the public API."""

from __future__ import annotations

import logging
import os
from typing import Dict

import requests

UNISWAP_API_URL = os.environ.get(
    "UNISWAP_API_URL",
    "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-polygon",
)
POOL_ADDRESS = os.environ.get("POOL_ADDRESS", "").lower()

QUERY = """
query ($id: ID!) {
  pool(id: $id) {
    sqrtPrice
    tick
    feeTier
    liquidity
  }
}
"""


def get_pool_data() -> Dict[str, int | float]:
    """Return basic data from the Uniswap API."""
    if not POOL_ADDRESS:
        raise RuntimeError("POOL_ADDRESS not configured")
    payload = {"query": QUERY, "variables": {"id": POOL_ADDRESS}}
    try:
        resp = requests.post(UNISWAP_API_URL, json=payload, timeout=10)
        resp.raise_for_status()
        pool = resp.json()["data"]["pool"]
        sqrt_price = float(pool["sqrtPrice"])
        tick = int(pool["tick"])
        liquidity = int(pool["liquidity"])
        fee = int(pool["feeTier"])
        price = (sqrt_price / (2**96)) ** 2
        return {"price": price, "tick": tick, "liquidity": liquidity, "fee": fee}
    except Exception as exc:  # pragma: no cover - external call
        logging.warning("Failed to fetch Uniswap data: %s", exc)
        return {"price": 0.0, "tick": 0, "liquidity": 0, "fee": 0}

