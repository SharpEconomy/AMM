"""
WSGI config for amm_controller project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import logging
import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amm_controller.settings")

application = get_wsgi_application()

# Run migrations on startup if possible
if os.environ.get("AUTO_MIGRATE", "1") == "1":
    try:
        call_command("migrate", interactive=False, verbosity=0)
    except Exception as exc:  # pragma: no cover - best effort
        logging.exception("Automatic migration failed", exc_info=exc)
