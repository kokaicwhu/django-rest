import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to pause execution until database is available"""

    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for database...')
        while True:
            try:
                connections['default'].connect()
                self.stdout.write(self.style.SUCCESS('Database available!'))
                return
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
            except Exception:
                self.stdout.write('Failed into trouble when connecting to database, waiting 1 second...')
                time.sleep(1)
