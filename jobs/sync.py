from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
import os

from dashboard.models import OpportunityLog, PriceSnapshot
from services.uniswap import get_pool_data
from services.cex_price import get_average_price

THRESHOLD = float(os.environ.get("PRICE_THRESHOLD", 1.0)) / 100

scheduler = BackgroundScheduler()


def sync_prices():
    uni_data = get_pool_data()
    avg, bm, cs = get_average_price()
    if avg is None:
        return

    uni_price = uni_data["price"]
    delta = abs(uni_price - avg) / avg
    PriceSnapshot.objects.create(
        timestamp=timezone.now(),
        uniswap_price=uni_price,
        bitmart_price=bm,
        coinstore_price=cs,
    )
    if delta > THRESHOLD:
        OpportunityLog.objects.create(
            timestamp=timezone.now(),
            delta_percent=delta * 100,
            uniswap_price=uni_price,
            average_price=avg,
        )


def start():
    scheduler.add_job(sync_prices, "interval", seconds=60)
    scheduler.start()
