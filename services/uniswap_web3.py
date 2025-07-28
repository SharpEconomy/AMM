"""Get Uniswap pool price via Web3."""

from __future__ import annotations

import os
from typing import Optional

from web3 import Web3

# Minimal ABI containing the slot0 view we need
UNISWAP_V3_POOL_ABI = [
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
            {"internalType": "bool", "name": "unlocked", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]

ALCHEMY_URL = os.environ.get("ALCHEMY_URL")
POOL_ADDRESS = (
    os.environ.get("UNISWAP_POOL_ADDRESS")
    or os.environ.get("POOL_ADDRESS")
)


def get_uniswap_price() -> Optional[float]:
    """Return SHARP/USDT price from Uniswap via Web3 or ``None`` on failure."""
    if not ALCHEMY_URL or not POOL_ADDRESS:
        return None
    try:
        web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
        pool = web3.eth.contract(
            address=Web3.to_checksum_address(POOL_ADDRESS),
            abi=UNISWAP_V3_POOL_ABI,
        )
        slot0 = pool.functions.slot0().call()
        sqrt_price_x96 = slot0[0]
        price = (sqrt_price_x96 / 2**96) ** 2
        return 1 / price if price else None
    except Exception:
        return None
