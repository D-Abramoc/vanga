import csv

from django.core.management.base import BaseCommand

# from vanga_back.backend import models


class Command(BaseCommand):
    help = 'Импорт данных из csv файла'

    def handle(self, *args, **options):
        with open(r'data/st_df.csv',
                  encoding='utf8') as csvfile:
            reader = csv.reader(csvfile)
            cities = set()
            divisions = set()
            print(reader)
            for row in reader:
                cities.add(row[1])
                divisions.add(row[2])
                # print(row[1], row[2])
                # print(len(cities), len(divisions))
