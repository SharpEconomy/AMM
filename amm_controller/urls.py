"""
URL configuration for amm_controller project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from dashboard import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/latest/", views.api_latest, name="api_latest"),
    path("api/opportunities/", views.api_opportunities, name="api_opportunities"),
    path("api/manual_sync/", views.api_manual_sync, name="api_manual_sync"),
    path("api/rebalance/", views.api_rebalance, name="api_rebalance"),
    path(
        "api/bitmart_price/",
        views.api_bitmart_price,
        name="api_bitmart_price",
    ),
    path(
        "api/coinstore_price/",
        views.api_coinstore_price,
        name="api_coinstore_price",
    ),
]
