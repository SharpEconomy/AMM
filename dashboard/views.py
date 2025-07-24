"""Views for the simple monitoring dashboard and authentication."""

import json
from typing import Callable, Any

from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from amm_controller import settings
import os

from .models import OpportunityLog, PriceSnapshot
from services.uniswap import get_pool_data
from services.cex_price import get_average_price
from jobs.sync import sync_prices
import pyotp


def _require_login(view: Callable[[HttpRequest], Any]) -> Callable[[HttpRequest], Any]:
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        if not request.session.get("authenticated"):
            return redirect("login")
        return view(request, *args, **kwargs)

    return wrapper


def login_view(request: HttpRequest) -> HttpResponse:
    """Render login page or handle login form submission."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        otp = request.POST.get("otp", "").strip()

        if not any(email.endswith("@" + d) for d in settings.ALLOWED_EMAIL_DOMAINS):
            return render(request, "login.html", {"error": "Invalid email"})

        totp = pyotp.TOTP(settings.OTP_SECRET)
        if not totp.verify(otp):
            return render(request, "login.html", {"error": "Invalid OTP"})

        request.session["authenticated"] = True
        request.session["name"] = name
        request.session["email"] = email
        return redirect("dashboard")

    return render(request, "login.html")


@csrf_exempt
def auto_login(request: HttpRequest) -> HttpResponse:
    """Auto-login endpoint using stored localStorage data."""
    if request.method != "POST":
        return HttpResponse(status=405)
    try:
        data = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    email = str(data.get("email", "")).lower()
    name = str(data.get("name", ""))
    if any(email.endswith("@" + d) for d in settings.ALLOWED_EMAIL_DOMAINS):
        request.session["authenticated"] = True
        request.session["name"] = name
        request.session["email"] = email
        return HttpResponse("OK")
    return HttpResponse(status=400)


def logout_view(request: HttpRequest) -> HttpResponse:
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


@_require_login
def api_latest(request: HttpRequest) -> JsonResponse:
    snap = PriceSnapshot.objects.order_by("-timestamp").first()
    if not snap:
        uni_data = get_pool_data()
        avg, bm, cs = get_average_price()
        snap = PriceSnapshot(
            timestamp=timezone.now(),
            uniswap_price=uni_data["price"],
            bitmart_price=bm,
            coinstore_price=cs,
        )
        snap.save()
    return JsonResponse(
        {
            "timestamp": snap.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "uniswap_price": snap.uniswap_price,
            "bitmart_price": snap.bitmart_price,
            "coinstore_price": snap.coinstore_price,
        }
    )


@_require_login
def api_opportunities(request: HttpRequest) -> JsonResponse:
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


@_require_login
@csrf_exempt
def api_manual_sync(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    sync_prices()
    return JsonResponse({"status": "ok"})


@_require_login
@csrf_exempt
def api_rebalance(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not os.environ.get("PRIVATE_KEY"):
        return JsonResponse({"message": "Read-only mode"})
    # Placeholder for actual contract interaction
    return JsonResponse({"message": "Rebalance executed"})
