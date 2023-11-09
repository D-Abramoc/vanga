import datetime
import os
from io import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd
import psycopg2.extras

from backend import models as m
from forecast.config import DS_URL
from forecast.functions import send_sales_to_ds


def establish_connection():
    """Подключение к базе данных"""
    print(f'{datetime.datetime.now()} / Установка соединения')
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    connection.autocommit = True
    return connection


def get_store_id(store):
    """Получение id магазина по хэшу"""
    return m.Shop.objects.get(st_id=store).id


def get_product_id(product):
    """Получение id товара по хэшу"""
    return m.Product.objects.get(pr_sku_id=product).id


def replace_shop_product_ids(df):
    """Замена хэшей магазинов и товаров на id"""
    print(f'{datetime.datetime.now()} / Замещение id магазинов в таблице')
    for store in df.st_id.unique():
        store_id = get_store_id(store)
        df.replace(to_replace=store, value=store_id, inplace=True)
    print(f'{datetime.datetime.now()} / Замещение id товаров в таблице')
    for product in df.pr_sku_id.unique():
        product_id = get_product_id(product)
        df.replace(to_replace=product, value=product_id, inplace=True)
    print(f'{datetime.datetime.now()} / Звершена подготовка таблицы')
    return df


def import_sales_df(filename: str, send: str) -> None:
    """Импорт данных о продажах"""
    connection = establish_connection()
    columns: tuple = ('st_id_id',
                      'pr_sku_id_id',
                      'date',
                      'pr_sales_type_id',
                      'pr_sales_in_units',
                      'pr_promo_sales_in_units',
                      'pr_sales_in_rub',
                      'pr_promo_sales_in_rub')
    print(f'{datetime.datetime.now()} / Чтение файла')
    sales = pd.read_csv(settings.BASE_DIR / f'data/{filename}')
    output = StringIO()
    print(f'{datetime.datetime.now()} / Подготовка данных')
    replace_shop_product_ids(sales).to_csv(output, header=False, index=False)
    output.seek(0)
    print(f'{datetime.datetime.now()} / Запись в БД')

    with connection.cursor() as cursor:
        cursor.copy_from(output, 'backend_sale', sep=',', columns=columns)
    print(f'{datetime.datetime.now()} / Импорт завершен')
    connection.close()

    if send == 'yes':
        send_sales_to_ds(sales, DS_URL)
        print('Данные отправлены на сервер DS')


class Command(BaseCommand):
    help = 'Команда: python manage.py import_sales filename.csv yes/no'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=str,
            help='Название импортируемого файла с указанием формата .csv'
        )
        parser.add_argument(
            'send',
            type=str,
            help='yes если отправлять на DS, no если нет'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        send = options['send']
        import_sales_df(filename, send)
