from django.apps import AppConfig
import os


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"

    def ready(self):
        if os.environ.get("RUN_SCHEDULER") == "1":
            from jobs import sync
            sync.start()
