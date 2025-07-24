"""App configuration for the dashboard app."""

import os
from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"

    def ready(self):
        if os.environ.get("RUN_SCHEDULER") == "1":
            from jobs import sync
            sync.start()
