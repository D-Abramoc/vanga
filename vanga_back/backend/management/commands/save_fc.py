import pandas as pd
from django.core.management.base import BaseCommand

from forecast.models import Forecast


def save_fc(date) -> None:
    """Сохранить файл с прогнозом"""
    forecasts = Forecast.objects.filter(calc_date=date)
    forecast_list = []
    for forecast in forecasts:
        forecast_list.append([forecast.st_id,
                             forecast.pr_sku_id,
                             forecast.date,
                             forecast.target])
    forecast_df = pd.DataFrame(forecast_list)
    writer = pd.ExcelWriter(f'data/{date}.xlsx')
    forecast_df.to_excel(writer, index=False)
    writer._save()


class Command(BaseCommand):
    help = 'Команда: python manage.py save_fc ГГГГ-ММ-ДД'

    def add_arguments(self, parser):
        parser.add_argument(
            'date',
            type=str,
            help='Дата прогноза ГГГГ-ММ-ДД'
        )

    def handle(self, *args, **options):
        date = options['date']
        save_fc(date)
