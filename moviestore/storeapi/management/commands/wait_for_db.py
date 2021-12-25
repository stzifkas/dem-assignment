"""
Django command to wait for the database to be ready.
"""
import time
import psycopg2
import os
from psycopg2 import OperationalError as Psycopg2OperationalError
from django.db.utils import OperationalError as DjangoOperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Django command to wait for the database to be ready.
    """
    def handle(self, *args, **kwargs):
        """
        Handle the command.
        """
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = psycopg2.connect(
                    dbname=os.environ.get('DB_NAME'),
                    user=os.environ.get('DB_USER'),
                    password=os.environ.get('DB_PASSWORD'),
                    host=os.environ.get('DB_HOST'),
                )
            except Psycopg2OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))