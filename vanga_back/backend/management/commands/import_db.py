import datetime
from io import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd

from backend import models as m
from backend.functions import establish_connection


def get_city_id(city) -> int:
    """Получение id магазина по хэшу"""
    return m.City.objects.get(city_id=city).id


def get_division_id(division) -> int:
    """Получение id товара по хэшу"""
    return m.Division.objects.get(division_code_id=division).id


def get_subcat_id(subcat) -> int:
    """Получение id товара по хэшу"""
    return m.Subcategory.objects.get(subcat_id=subcat).id


def replace_city_division_ids(df):
    """Замена хэшей магазинов и товаров на id"""
    print(f'{datetime.datetime.now()} / Замещение id городов в таблице')
    for city in df.st_city_id.unique():
        city_id = get_city_id(city)
        df.loc[df['st_city_id'] == city, 'st_city_id'] = city_id
    print(f'{datetime.datetime.now()} / Замещение id дивизионов в таблице')
    for div in df.st_division_code.unique():
        div_id = get_division_id(div)
        df.loc[df['st_division_code'] == div, 'st_division_code'] = div_id
    print(f'{datetime.datetime.now()} / Звершена подготовка таблицы')
    return df


def get_parent_category(df, child_name, child_id, parent_name):
    """Получение родительской категории для подкатегории"""
    row = (df.loc[df[child_name] == child_id])
    return row[parent_name].unique()[0]


def replace_subcategory_ids(df):
    """Замена хэшей магазинов и товаров на id"""
    print(f'{datetime.datetime.now()} / Замещение id подкатегорий в таблице')
    for subcat in df.pr_subcat_id.unique():
        subcat_id = get_subcat_id(subcat)
        df.loc[df['pr_subcat_id'] == subcat, 'pr_subcat_id'] = subcat_id
    del df['pr_group_id']
    del df['pr_cat_id']
    print(f'{datetime.datetime.now()} / Звершена подготовка таблицы')
    return df


def import_pr_df_csv() -> None:
    """Импорт групп, категорий, подкатегорий и товаров"""
    connection = establish_connection()
    print(f'{datetime.datetime.now()} / Чтение файла pr_df.csv')
    pr_df = pd.read_csv(settings.BASE_DIR / r'data/pr_df.csv')

    groups, categories, subcategories = [], [], []

    print(f'{datetime.datetime.now()} / Запись групп товаров в БД')
    for pr_group_id in pr_df.pr_group_id.unique():
        groups.append(m.Group(group_id=pr_group_id))
    m.Group.objects.bulk_create(groups)

    print(f'{datetime.datetime.now()} / Запись категорий товаров в БД')
    for pr_cat_id in pr_df.pr_cat_id.unique():
        group_id = get_parent_category(pr_df,
                                       'pr_cat_id',
                                       pr_cat_id,
                                       'pr_group_id')
        categories.append(m.Category(
            group_id=m.Group.objects.get(group_id=group_id),
            cat_id=pr_cat_id))
    m.Category.objects.bulk_create(categories)

    print(f'{datetime.datetime.now()} / Запись подкатегорий товаров в БД')
    for pr_subcat_id in pr_df.pr_subcat_id.unique():
        cat_id = get_parent_category(pr_df,
                                     'pr_subcat_id',
                                     pr_subcat_id,
                                     'pr_cat_id')
        subcategories.append(m.Subcategory(
            cat_id=m.Category.objects.get(cat_id=cat_id),
            subcat_id=pr_subcat_id))
    m.Subcategory.objects.bulk_create(subcategories)

    products = StringIO()
    replace_subcategory_ids(pr_df).to_csv(products, header=False, index=False)
    products.seek(0)
    columns: tuple = ('pr_sku_id',
                      'pr_subcat_id_id',
                      'pr_uom_id')

    print(f'{datetime.datetime.now()} / Запись товаров в БД')
    with connection.cursor() as cursor:
        cursor.copy_from(products, 'backend_product', sep=',', columns=columns)
    print(f'{datetime.datetime.now()} / Импорт pr_df.csv завершен')

    connection.close()


def import_st_df_csv() -> None:
    """Импорт городов, дивизионов и магазинов"""
    connection = establish_connection()
    print(f'{datetime.datetime.now()} / Чтение файла st_df.csv')
    st_df = pd.read_csv(settings.BASE_DIR / r'data/st_df.csv')

    cities = StringIO()
    df = pd.DataFrame(st_df['st_city_id'].unique())
    df.to_csv(cities, header=False, index=False)
    cities.seek(0)

    divisions = StringIO()
    df = pd.DataFrame(st_df['st_division_code'].unique())
    df.to_csv(divisions, header=False, index=False)
    divisions.seek(0)

    print(f'{datetime.datetime.now()} / Запись городов и дивизионов в БД')
    with connection.cursor() as cursor:
        cursor.copy_from(cities, 'backend_city', columns=['city_id'])
        cursor.copy_from(divisions, 'backend_division', columns=['division_code_id'])

    shops = StringIO()
    replace_city_division_ids(st_df).to_csv(shops, header=False, index=False)
    shops.seek(0)
    columns: tuple = ('st_id',
                      'st_city_id_id',
                      'st_division_code_id_id',
                      'st_type_format_id',
                      'st_type_loc_id',
                      'st_type_size_id',
                      'st_is_active')

    print(f'{datetime.datetime.now()} / Запись магазинов в БД')
    with connection.cursor() as cursor:
        cursor.copy_from(shops, 'backend_shop', sep=',', columns=columns)
    print(f'{datetime.datetime.now()} / Импорт st_df.csv завершен')

    connection.close()


class Command(BaseCommand):
    help = 'Команда: python manage.py import_db'

    def handle(self, *args, **options):
        import_st_df_csv()
        import_pr_df_csv()
