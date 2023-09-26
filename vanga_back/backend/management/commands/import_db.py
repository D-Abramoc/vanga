import pandas as pd

from django.core.management.base import BaseCommand

from backend import models as m

class Command(BaseCommand):
    help = 'Импорт данных в базу'

    def import_st_df_csv(self):
        """Импорт городов, дивизионов и магазинов"""
        st_df = pd.read_csv(r'data/st_df.csv')
        cities, divisions, shops = [], [], []

        for city_id in st_df.st_city_id.unique():
            cities.append(m.City(city_id=city_id))
        m.City.objects.bulk_create(cities)
        print('Импорт городов завершён')

        for st_division_code in st_df.st_division_code.unique():
            divisions.append(m.Division(division_code_id=st_division_code))
        m.Division.objects.bulk_create(divisions)
        print('Импорт дивизионов завершён')

        for _, row in st_df.iterrows():
            shops.append(m.Shop(
                st_id=row['st_id'],
                st_city_id=m.City.objects.get(city_id=row['st_city_id']),
                st_division_code_id=m.Division.objects.get(
                    division_code_id=row['st_division_code']
                ),
                st_type_format_id=row['st_type_format_id'],
                st_type_loc_id=row['st_type_loc_id'],
                st_type_size_id=row['st_type_size_id'],
                st_is_active=row['st_is_active'],)
            )
        m.Shop.objects.bulk_create(shops)
        print('Импорт магазинов завершён')

    def import_pr_df_csv(self):
        """Групп, категорий, подкатегорий и товаров"""
        pr_df = pd.read_csv(r'data/pr_df.csv')
        groups, categories, subcategories, products = [], [], [], []

        for pr_group_id in pr_df.pr_group_id.unique():
            groups.append(m.Group(group_id=pr_group_id))
        m.Group.objects.bulk_create(groups)
        print('Импорт групп завершён.')

        def get_parent_category(df, child_name, child_id, parent_name):
            """Получение родительской категории для подкатегории"""
            row = (df.loc[df[child_name] == child_id])
            return row[parent_name].unique()[0]

        for pr_cat_id in pr_df.pr_cat_id.unique():
            group_id = get_parent_category(pr_df,
                                           'pr_cat_id',
                                           pr_cat_id,
                                           'pr_group_id')
            categories.append(m.Category(
                group_id=m.Group.objects.get(group_id=group_id),
                cat_id=pr_cat_id))
        m.Category.objects.bulk_create(categories)
        print('Импорт категорий завершён.')

        for pr_subcat_id in pr_df.pr_subcat_id.unique():
            cat_id = get_parent_category(pr_df,
                                           'pr_subcat_id',
                                           pr_subcat_id,
                                           'pr_cat_id')
            subcategories.append(m.Subcategory(
                cat_id=m.Category.objects.get(cat_id=cat_id),
                subcat_id=pr_subcat_id))
        m.Subcategory.objects.bulk_create(subcategories)
        print('Импорт подкатегорий завершён.')

        for _, row in pr_df.iterrows():
            uom_id = 0 if row['pr_uom_id'] == 17 else 1
            products.append(m.Product(
                pr_sku_id=row['pr_sku_id'],
                pr_subcat_id=m.Subcategory.objects.get(subcat_id=row['pr_subcat_id']),
                pr_uom_id=uom_id)
            )
        m.Product.objects.bulk_create(products)
        print('Импорт магазинов завершён.')

    def handle(self, *args, **options):
        self.import_st_df_csv()
        self.import_pr_df_csv()
