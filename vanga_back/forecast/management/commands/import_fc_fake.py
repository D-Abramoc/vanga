from django.conf import settings
from django.core.management.base import BaseCommand

import pandas as pd
from backend import models as m
from forecast.models import Forecast


def import_forecast():
    """Импорт прогнозных данных"""
    fc_data = pd.read_csv(settings.BASE_DIR / r'data/forecast_fake.csv')
    forecasts = []
    calc_date = '2023-07-18'

    for index, row in fc_data.iterrows():
        forecasts.append(Forecast(
            calc_date=calc_date,
            st_id=m.Shop.objects.get(st_id=row['st_id']),
            pr_sku_id=m.Product.objects.get(pr_sku_id=row['pr_sku_id']),
            date=row['date'],
            target=row['target']))
    Forecast.objects.bulk_create(forecasts)
    print('Импорт прогнозов завершён.')


class Command(BaseCommand):
    help = 'Команда: python manage.py import_fc'

    def handle(self, *args, **options):
        import_forecast()
