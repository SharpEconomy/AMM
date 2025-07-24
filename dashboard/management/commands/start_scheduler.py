"""Management command to run the APScheduler worker."""

from django.core.management.base import BaseCommand
from jobs import sync


class Command(BaseCommand):
    help = "Starts APScheduler"

    def handle(self, *args, **options):
        sync.start()
        self.stdout.write(self.style.SUCCESS("Scheduler started"))
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
