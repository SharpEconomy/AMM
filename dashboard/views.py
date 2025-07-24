"""Views for the monitoring dashboard."""

from __future__ import annotations

import os
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import OpportunityLog, PriceSnapshot, DashboardUser
from services.uniswap import get_pool_data
from services.cex_price import get_average_price
from jobs.sync import sync_prices


def logout_view(request: HttpRequest) -> HttpResponse:
    """Clear the session and redirect to login."""

    request.session.flush()
    return redirect("login")


@_require_login
def dashboard(request: HttpRequest) -> HttpResponse:
    """Render dashboard page."""
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


def api_latest(request: HttpRequest) -> JsonResponse:
    """Return the most recent price snapshot, creating one if necessary."""

    snap = PriceSnapshot.objects.order_by("-timestamp").first()
    if not snap:
        uni_data = get_pool_data()
        _, bm, cs = get_average_price()
        snap = PriceSnapshot.objects.create(
            timestamp=timezone.now(),
            uniswap_price=uni_data["price"],
            bitmart_price=bm,
            coinstore_price=cs,
        )
    return JsonResponse(
        {
            "timestamp": snap.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "uniswap_price": snap.uniswap_price,
            "bitmart_price": snap.bitmart_price,
            "coinstore_price": snap.coinstore_price,
        }
    )


def api_opportunities(request: HttpRequest) -> JsonResponse:
    """Return recent logged opportunities."""

    ops = OpportunityLog.objects.order_by("-timestamp")[:20]
    data = [
        {
            "timestamp": o.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "delta_percent": o.delta_percent,
            "uniswap_price": o.uniswap_price,
            "average_price": o.average_price,
        }
        for o in ops
    ]
    return JsonResponse(data, safe=False)

@require_POST
def api_manual_sync(request: HttpRequest) -> JsonResponse:
    """Trigger an immediate price sync."""

    sync_prices()
    return JsonResponse({"status": "ok"})


@require_POST
def api_rebalance(request: HttpRequest) -> JsonResponse:
    """Execute a rebalance action if a private key is configured."""

    if not os.environ.get("PRIVATE_KEY"):
        return JsonResponse({"message": "Read-only mode"})
    # Placeholder for actual contract interaction
    return JsonResponse({"message": "Rebalance executed"})
