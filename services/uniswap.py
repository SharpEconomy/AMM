"""Utilities for reading Uniswap V3 pool data."""

from __future__ import annotations

from functools import lru_cache
import logging
import os
from typing import Dict, Optional

from web3 import Web3

RPC_URL = os.environ.get("RPC_URL") or os.environ.get("ALCHEMY_URL")
POOL_ADDRESS = os.environ.get("POOL_ADDRESS")
if POOL_ADDRESS:
    POOL_ADDRESS = Web3.to_checksum_address(POOL_ADDRESS)

POOL_ABI = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
            {"internalType": "int24", "name": "tick", "type": "int24"},
            {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
            {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
            {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
            {"internalType": "bool", "name": "unlocked", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {"inputs": [], "name": "liquidity", "outputs": [{"internalType": "uint128", "name": "", "type": "uint128"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "fee", "outputs": [{"internalType": "uint24", "name": "", "type": "uint24"}], "stateMutability": "view", "type": "function"}
]


web3: Optional[Web3] = None
if RPC_URL:
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
else:  # pragma: no cover - runtime check
    logging.warning("RPC_URL not configured; Uniswap data disabled")


@lru_cache(maxsize=1)
def get_pool_contract():
    """Return a cached contract instance for the configured pool."""
    if not web3 or not POOL_ADDRESS:
        raise RuntimeError("Uniswap configuration missing")
    return web3.eth.contract(address=POOL_ADDRESS, abi=POOL_ABI)


def get_pool_data() -> Dict[str, int | float]:
    """Return basic data from the pool contract."""
    try:
        contract = get_pool_contract()
        slot0 = contract.functions.slot0().call()
        liquidity = contract.functions.liquidity().call()
        fee = contract.functions.fee().call()
        sqrt_price_x96 = slot0[0]
        tick = slot0[1]
        price = (sqrt_price_x96 / (2**96))**2
        return {
            "price": price,
            "tick": tick,
            "liquidity": liquidity,
            "fee": fee,
        }
    except Exception as exc:  # pragma: no cover - external call
        logging.warning("Failed to fetch Uniswap data: %s", exc)
        return {"price": 0.0, "tick": 0, "liquidity": 0, "fee": 0}

