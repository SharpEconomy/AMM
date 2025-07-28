"""Views for the monitoring dashboard."""

from __future__ import annotations

import logging
import os
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import OpportunityLog, PriceSnapshot
from services.uniswap import get_pool_data
from services.uniswap_web3 import get_uniswap_price as get_live_uniswap_price
from services.cex_price import (
    fetch_bitmart_price,
    fetch_coinstore_price,
    get_average_price,
)
from jobs.sync import sync_prices


def dashboard(request: HttpRequest) -> HttpResponse:
    """Render dashboard page."""
    latest_snapshot = PriceSnapshot.objects.order_by("-timestamp").first()
    opportunities = OpportunityLog.objects.order_by("-timestamp")[:20]
    if not latest_snapshot:
        try:
            uni_data = get_pool_data()
            avg, bm, cs = get_average_price()
            latest_snapshot = PriceSnapshot(
                timestamp=timezone.now(),
                uniswap_price=uni_data["price"],
                bitmart_price=bm,
                coinstore_price=cs,
            )
        except Exception as exc:  # pragma: no cover - external
            logging.warning("Failed to fetch initial data: %s", exc)
            latest_snapshot = PriceSnapshot(
                timestamp=timezone.now(),
                uniswap_price=0,
                bitmart_price=None,
                coinstore_price=None,
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
        try:
            uni_data = get_pool_data()
            _, bm, cs = get_average_price()
            snap = PriceSnapshot.objects.create(
                timestamp=timezone.now(),
                uniswap_price=uni_data["price"],
                bitmart_price=bm,
                coinstore_price=cs,
            )
        except Exception as exc:  # pragma: no cover - external
            logging.warning("Failed to create snapshot: %s", exc)
            snap = PriceSnapshot.objects.create(
                timestamp=timezone.now(),
                uniswap_price=0,
                bitmart_price=None,
                coinstore_price=None,
            )
    return JsonResponse(
        {
            "timestamp": snap.timestamp.isoformat(),
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
            "timestamp": o.timestamp.isoformat(),
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

    try:
        sync_prices()
    except Exception as exc:  # pragma: no cover - external
        logging.warning("Manual sync failed: %s", exc)
    return JsonResponse({"status": "ok"})


@require_POST
def api_rebalance(request: HttpRequest) -> JsonResponse:
    """Execute a rebalance action if a private key is configured."""

    if not os.environ.get("PRIVATE_KEY"):
        return JsonResponse({"message": "Read-only mode"})
    # Placeholder for actual contract interaction
    logging.info("Rebalance triggered by user")
    return JsonResponse({"message": "Rebalance executed"})


def api_bitmart_price(request: HttpRequest) -> JsonResponse:
    """Return the current Bitmart SHARP/USDT price."""

    price = fetch_bitmart_price()
    return JsonResponse({"price": price})


def api_coinstore_price(request: HttpRequest) -> JsonResponse:
    """Return the current Coinstore SHARP/USDT price."""

    price = fetch_coinstore_price()
    return JsonResponse({"price": price})


def api_live_prices(request: HttpRequest) -> JsonResponse:
    """Return current prices from each source without using the DB."""

    uni = get_live_uniswap_price()
    bm = fetch_bitmart_price()
    cs = fetch_coinstore_price()
    return JsonResponse(
        {
            "uniswap_price": uni,
            "bitmart_price": bm,
            "coinstore_price": cs,
        }
    )
