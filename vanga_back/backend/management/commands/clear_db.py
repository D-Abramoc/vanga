from backend import models as m
from forecast.models import Forecast
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Удаление всех объектов из БД'

    def handle(self, *args, **options):
        # m.City.objects.all().delete()
        # m.Division.objects.all().delete()
        # m.Shop.objects.all().delete()
        # m.Group.objects.all().delete()
        # m.Category.objects.all().delete()
        # m.Subcategory.objects.all().delete()
        # m.Product.objects.all().delete()
        m.Sale.objects.all().delete()
        # Forecast.objects.all().delete()
        print('База очищена')
