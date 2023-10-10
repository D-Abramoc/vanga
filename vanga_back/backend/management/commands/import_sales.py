from time import sleep

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from backend import models as m
from forecast.config import DS_URL
from forecast.functions import get_forecast, send_sales_to_ds

BATCH_SIZE = 10000
SLEEP_TIME = 480


def import_sales_df(filename) -> None:
    """Импорт данных о продажах"""
    sales_df = pd.read_csv(settings.BASE_DIR / f'data/{filename}',
                           dtype={'st_id': 'category',
                                  'pr_sku_id': 'category',
                                  'pr_sales_type_id': 'int64',
                                  'pr_sales_in_units': 'int64',
                                  'pr_promo_sales_in_units': 'int64',
                                  'pr_sales_in_rub': 'int64',
                                  'pr_promo_sales_in_rub': 'int64',
                                  },
                           parse_dates=['date']
                           )

    sales = []
    imported_rows = 0

    for index, row in sales_df.iterrows():
        sales.append(m.Sale(
            st_id=m.Shop.objects.get(st_id=row['st_id']),
            pr_sku_id=m.Product.objects.get(pr_sku_id=row['pr_sku_id']),
            date=row['date'],
            pr_sales_type_id=row['pr_sales_type_id'],
            pr_sales_in_units=row['pr_sales_in_units'],
            pr_promo_sales_in_units=row['pr_promo_sales_in_units'],
            pr_sales_in_rub=row['pr_sales_in_rub'],
            pr_promo_sales_in_rub=row['pr_promo_sales_in_rub'])
        )
        if len(sales) == BATCH_SIZE:
            m.Sale.objects.bulk_create(sales)
            send_sales_to_ds(sales)
            sales = []
            imported_rows += BATCH_SIZE
            print(f'Импортировано {imported_rows} строк данных о продажах')
    m.Sale.objects.bulk_create(sales)
    print('Импорт продаж завершён')
    send_sales_to_ds(sales, DS_URL)
    print('Данные отправлены на сервер DS')
    print(f'Start sleep {SLEEP_TIME} seconds')
    sleep(SLEEP_TIME)
    print('Stop sleep, запрос прогноза')
    get_forecast()
    print('Прогноз получен')


class Command(BaseCommand):
    help = 'Команда: python manage.py import_sales filename.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=str,
            help='Название импортируемого файла с указанием формата .csv'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        import_sales_df(filename)
