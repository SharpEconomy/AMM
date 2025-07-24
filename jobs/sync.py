"""Background task for fetching prices and logging opportunities."""

import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from dashboard.models import OpportunityLog, PriceSnapshot
from services.uniswap import get_pool_data
from services.cex_price import get_average_price

THRESHOLD = float(os.environ.get("PRICE_THRESHOLD", 1.0)) / 100
INTERVAL = int(os.environ.get("SYNC_INTERVAL_SECONDS", "60"))

scheduler = BackgroundScheduler()


def sync_prices() -> None:
    """Fetch prices from DEX and CEX and log large deltas."""
    uni_data = get_pool_data()
    avg, bm, cs = get_average_price()

    uni_price = uni_data["price"]
    PriceSnapshot.objects.create(
        timestamp=timezone.now(),
        uniswap_price=uni_price,
        bitmart_price=bm,
        coinstore_price=cs,
    )

    if avg is None:
        return

    delta = abs(uni_price - avg) / avg
    if delta > THRESHOLD:
        OpportunityLog.objects.create(
            timestamp=timezone.now(),
            delta_percent=delta * 100,
            uniswap_price=uni_price,
            average_price=avg,
        )


def start() -> None:
    """Start the background scheduler if not already running."""
    if not scheduler.running:
        scheduler.add_job(sync_prices, "interval", seconds=INTERVAL)
        scheduler.start()
