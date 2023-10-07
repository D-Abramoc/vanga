from http import HTTPStatus
from rest_framework.test import APIClient, APITestCase
from users.models import User
from backend.models import Shop, Product, Sale

from backend.management.commands import (
    import_db, import_sales
)

import psycopg2

BATCH_SIZE = 10000

def insert_execute_batch(connection, beers) -> None:
    with connection.cursor() as cursor:

        psycopg2.extras.execute_batch(cursor, """
            INSERT INTO  VALUES (
                %(st_id)r,
                %(pr_sku_id)r,
                %(pr_sales_type_id)r,
                %(pr_sales_in_units)r,
                %(pr_promo_sales_in_units)r,
                %(pr_sales_in_rub)r,
                %(pr_promo_sales_in_rub)r,
            );
        """, beers)


class ApiTest(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        import_db.import_st_df_csv()
        import_db.import_pr_df_csv()
        import_sales.import_sales_df('sales_df_train.csv')

    def setUp(self) -> None:
        self.client = APIClient()
        # connection = psycopg2.connect(
        #     host='localhost',
        #     database='test_vanga_1',
        #     user='vanga',
        #     password='admin'
        # )
        # connection.autocommit = True
        # with open(r'/home/abramov/Dev/vanga/vanga_back/data/pr_df.csv', 'r') as f:
        #     f.__next__
        #     insert_execute_batch(connection, f)

    def test_create_user(self):
        '''Регистрация пользователя'''
        number_users = User.objects.count()
        data = {
            'email': 'gector_barbossa@black.perl',
            'password': 'pass_word'
        }
        # Регистрация нового пользователя
        response = self.client.post('/api/auth/users/', data)
        self.assertEqual(User.objects.count(), number_users + 1)
        # Дублирование пользователя
        response = self.client.post('/api/auth/users/', data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(User.objects.count(), number_users + 1)

    def test_import_db(self):
        print(f'Stores : {Product.objects.count()}')
        print(f'Sales: {Sale.objects.count()}')

    def test_filter_group(self):
        response = self.client.get('/api/v1/filters/groups_whith_sales/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Shop.objects.count())
        for shop in response.data:
            print(shop)
            with self.subTest(msg=f'{shop["id"]}', shop=shop):
                for group in shop['groups']:
                    print(group)
                    with self.subTest(msg=f'{group["id"]}', group=group):
                        self.assertEqual(
                            (Product.objects.filter(
                                sales__st_id=shop['id'],
                                pr_subcat_id__cat_id__group_id=group['id']
                            ).exists()), True
                        )

    def test_filter_category(self):
        response = self.client.get('/api/v1/filters/groups_whith_sales/')
        for shop in response.data:
            for group in shop['groups']:
                response = self.client.get(
                    f'/api/v1/filters/categories_with_sales/?store={shop["id"]}&group={group["id"]}'
                )
                self.assertEqual(response.status_code, 200)
                for category in response.data[0]['groups'][0]['categories']:
                    with self.subTest(msg=f'*{shop["id"]}*{group["id"]}*{category["id"]}', category=category):
                        self.assertEqual(
                            (Product.objects
                             .filter(
                                sales__pr_sales_type_id=False,
                                sales__st_id=shop['id'],
                                pr_subcat_id__cat_id__group_id=group['id'],
                                pr_subcat_id__cat_id=category['id']
                                ).exists()
                            ), True
                        )

    def test_filter_category2(self):
        response = self.client.get('/api/v1/filters/groups_whith_sales/')
        for shop in response.data:
            for group in shop['groups']:
                response = self.client.get(
                    f'/api/v1/filters/category/?store={shop["id"]}&group={group["id"]}'
                )
                self.assertEqual(response.status_code, 200)
                for category in response.data:
                    with self.subTest(msg=f'*{shop["id"]}*{group["id"]}*{category["id"]}', category=category):
                        self.assertEqual(
                            (Product.objects
                             .filter(
                                sales__pr_sales_type_id=False,
                                sales__st_id=shop['id'],
                                pr_subcat_id__cat_id__group_id=group['id'],
                                pr_subcat_id__cat_id=category['id']
                                ).exists()
                            ), True
                        )

