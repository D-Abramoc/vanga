from django.core.management.base import BaseCommand

from forecast.functions import get_forecast


class Command(BaseCommand):
    help = 'Команда: python manage.py update_forecast'

    def handle(self, *args, **options):
        get_forecast()
