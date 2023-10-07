import pandas as pd
from forecast.models import Forecast
from backend import models as m
from django.core.management.base import BaseCommand
from datetime import datetime


def import_forecast():
    """Импорт прогнозных данных"""
    fc_data = pd.read_csv(r'data/2023-07-18.csv')
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
