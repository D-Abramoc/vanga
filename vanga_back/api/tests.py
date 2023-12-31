from http import HTTPStatus

from rest_framework.test import APIClient, APITestCase

from backend.management.commands import import_db, import_sales_fake
from backend.models import Product, Shop
from forecast.management.commands import import_fc_fake
from users.models import User

BATCH_SIZE = 10000


class ApiTest(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        import_db.import_st_df_csv()
        import_db.import_pr_df_csv()
        import_sales_fake.import_sales_df('sales_df_train_fake.csv')
        import_fc_fake.import_forecast()

    def setUp(self) -> None:
        self.client = APIClient()
        self.auth_client = APIClient()
        data = {
            'email': 'pirat@fake.fake',
            'password': 'pass_word'
        }
        self.auth_client.post(
            '/api/auth/users/', data=data
        )
        self.auth_client.force_authenticate(
            User.objects.get(username='pirat@fake.fake')
        )

    def test_cities(self):
        response = self.auth_client.get(
            '/api/v1/cities/'
        )
        self.assertEqual(response.status_code, 200)

    def test_auth(self):
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
        # Получение токенов
        data = {
            'username': 'gector_barbossa@black.perl',
            'password': 'pass_word'
        }
        response = self.auth_client.post(
            '/api/auth/jwt/create/', data=data
        )
        refresh, access = response.data
        expected_keys = ('refresh', 'access',)
        for key in response.data.keys():
            with self.subTest(key=key):
                self.assertTrue(key in expected_keys)
        # Get current user
        self.auth_client.force_authenticate(
            user=User.objects.get(username=data['username'])
        )
        response = self.auth_client.get(
            '/api/auth/users/me/'
        )
        self.assertEqual(
            response.data['email'],
            User.objects.get(username=data['username']).email
        )
        # Refresh access token
        response = self.auth_client.post(
            '/api/auth/jwt/refresh/', data=refresh
        )
        new_access = response.data.values()
        self.assertNotEquals(new_access, access)
        # logout
        self.auth_client.post(
            '/api/auth/logout/', data=refresh
        )
        response = self.auth_client.post(
            '/api/auth/jwt/refresh/', data=refresh
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST
        )

    def test_filter_group(self):
        response = self.auth_client.get('/api/v1/filters/groups_whith_sales/')
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
        response = self.auth_client.get('/api/v1/filters/groups_whith_sales/')
        for shop in response.data:
            for group in shop['groups']:
                response = self.auth_client.get(
                    (f'/api/v1/filters/categories_with_sales/'
                     f'?store={shop["id"]}&group={group["id"]}')
                )
                self.assertEqual(response.status_code, 200)
                for category in response.data[0]['groups'][0]['categories']:
                    with self.subTest(category=category):
                        self.assertEqual(
                            (Product.objects
                             .filter(
                                sales__pr_sales_type_id=False,
                                sales__st_id=shop['id'],
                                pr_subcat_id__cat_id__group_id=group['id'],
                                pr_subcat_id__cat_id=category['id']
                                ).exists()), True
                        )

    def test_filter_category2(self):
        response = self.auth_client.get('/api/v1/filters/groups_whith_sales/')
        for shop in response.data:
            for group in shop['groups']:
                response = self.auth_client.get(
                    (f'/api/v1/filters/category/'
                     f'?store={shop["id"]}&group={group["id"]}')
                )
                self.assertEqual(response.status_code, 200)
                for category in response.data:
                    with self.subTest(category=category):
                        self.assertEqual(
                            (Product.objects.filter(
                                sales__pr_sales_type_id=False,
                                sales__st_id=shop['id'],
                                pr_subcat_id__cat_id__group_id=group['id'],
                                pr_subcat_id__cat_id=category['id']
                                ).exists()), True
                        )

    def test_filter_subcat(self):
        response = self.auth_client.get('/api/v1/filters/groups_whith_sales/')
        for shop in response.data:
            for group in shop['groups']:
                response = self.auth_client.get(
                    (f'/api/v1/filters/category/'
                     f'?store={shop["id"]}&group={group["id"]}')
                )
                for category in response.data:
                    response = self.auth_client.get(
                        (f'/api/v1/filters/subcategories_with_sales/'
                         f'?store={shop["id"]}&group={group["id"]}'
                         f'&category={category["id"]}')
                    )
                    for subcat in (
                        response.data[0]['categories'][0]['subcategories']
                    ):
                        with self.subTest(subcat=subcat):
                            self.assertTrue(
                                (Product.objects.filter(
                                    sales__pr_sales_type_id=False,
                                    sales__st_id=shop['id'],
                                    pr_subcat_id__cat_id__group_id=group['id'],
                                    pr_subcat_id__cat_id=category['id'],
                                    pr_subcat_id=subcat["id"]
                                ).exists())
                            )

    def test_filter_product(self):
        response = self.auth_client.get('/api/v1/filters/groups_whith_sales/')
        for shop in response.data:
            for group in shop['groups']:
                response = self.auth_client.get(
                    (f'/api/v1/filters/category/'
                     f'?store={shop["id"]}&group={group["id"]}')
                )
                for category in response.data:
                    response = self.auth_client.get(
                        (f'/api/v1/filters/subcategories_with_sales/'
                         f'?store={shop["id"]}&group={group["id"]}'
                         f'&category={category["id"]}')
                    )
                    for subcat in (
                        response.data[0]['categories'][0]['subcategories']
                    ):
                        response = self.auth_client.get(
                            (f'/api/v1/filters/products/'
                             f'?store={shop["id"]}&group={group["id"]}'
                             f'&category={category["id"]}'
                             f'&subcategory={subcat["id"]}')
                        )
                        self.assertTrue(response.data)

    def test_get_forecast(self):
        response = self.auth_client.get(
            '/api/v1/forecast/get_forecast/?store=12&product=1706'
        )
        self.assertTrue(response.data)
        response = self.auth_client.get(
            '/api/v1/forecast/get_forecast/?store=12&product=170'
        )
        self.assertFalse(response.data)
