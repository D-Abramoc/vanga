from django.core.management.base import BaseCommand

from backend import models as m
from forecast.models import Forecast


DB_TABLES = {'city': m.City,
             'division': m.Division,
             'shop': m.Shop,
             'group': m.Group,
             'category': m.Category,
             'subcategory': m.Subcategory,
             'product': m.Product,
             'sale': m.Sale,
             'forecast': Forecast,
             }


class Command(BaseCommand):
    help = 'Удаление всех объектов из БД'

    def add_arguments(self, parser):
        parser.add_argument(
            'table_name',
            nargs='+',
            type=str,
            help=('Таблицы, из которых требуется удалить объекты. '
                  'all для очистки всех таблиц. Варианты: city, division, '
                  'shop, group, category, subcategory, product, sale, '
                  'forecast.')
        )

    def handle(self, *args, **options):
        if 'all' in options['table_name']:
            for value in DB_TABLES.values():
                value.objects.all().delete()
            print('База очищена')
        else:
            tables = options['table_name']
            for table in tables:
                try:
                    DB_TABLES[table].objects.all().delete()
                    print(f'Таблица {table} очищена')
                except KeyError:
                    print(f'Таблица {table} не найдена')
