"""Views for the simple monitoring dashboard."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import OpportunityLog, PriceSnapshot
from services.uniswap import get_pool_data
from services.cex_price import get_average_price


def dashboard(request: HttpRequest) -> HttpResponse:
    """Render the dashboard with the latest price snapshot."""
    latest_snapshot = PriceSnapshot.objects.order_by("-timestamp").first()
    opportunities = OpportunityLog.objects.order_by("-timestamp")[:20]
    if not latest_snapshot:
        uni_data = get_pool_data()
        avg, bm, cs = get_average_price()
        latest_snapshot = PriceSnapshot(
            timestamp=timezone.now(),
            uniswap_price=uni_data["price"],
            bitmart_price=bm,
            coinstore_price=cs,
        )
    context = {
        "snapshot": latest_snapshot,
        "opportunities": opportunities,
    }
    return render(request, "dashboard.html", context)
