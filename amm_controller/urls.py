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

from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("auto_login/", views.auto_login, name="auto_login"),
    path("api/latest/", views.api_latest, name="api_latest"),
    path("api/opportunities/", views.api_opportunities, name="api_opportunities"),
    path("api/manual_sync/", views.api_manual_sync, name="api_manual_sync"),
    path("api/rebalance/", views.api_rebalance, name="api_rebalance"),
]
