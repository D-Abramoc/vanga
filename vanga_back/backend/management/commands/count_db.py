from backend import models as m
from forecast.models import Forecast
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Подсчет количества записей в БД'

    def handle(self, *args, **options):
        print('Город:', m.City.objects.all().count())
        print('Дивизион:', m.Division.objects.all().count())
        print('Магазин:', m.Shop.objects.all().count())
        print('Группа:', m.Group.objects.all().count())
        print('Категория:', m.Category.objects.all().count())
        print('Подкатегория:', m.Subcategory.objects.all().count())
        print('Товар:', m.Product.objects.all().count())
        print('Продажа:', m.Sale.objects.all().count())
        print('Прогноз:', Forecast.objects.all().count())
