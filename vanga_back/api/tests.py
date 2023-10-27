from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.test import APIClient, APITestCase

from backend.management.commands import import_db, import_sales_fake
from backend.models import Product, Shop, City, Division, Group, Category, Subcategory, Sale
from forecast.models import Forecast
from forecast.management.commands import import_fc_fake
from users.models import User

BATCH_SIZE = 10000


class ApiTest(APITestCase):
    # @classmethod
    # def setUpClass(cls) -> None:
    #     super().setUpClass()
    #     import_db.import_st_df_csv()
    #     import_db.import_pr_df_csv()
    #     import_sales_fake.import_sales_df('sales_df_train_fake.csv')
    #     import_fc_fake.import_forecast()
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        City.objects.create(
            city_id='Moscow'
        )
        City.objects.create(
            city_id='Kemerovo'
        )
        Division.objects.create(
            division_code_id='first_division'
        )
        Division.objects.create(
            division_code_id='second_division'
        )
        Group.objects.create(
            group_id='first_group'
        )
        Group.objects.create(
            group_id='second_group'
        )
        Category.objects.create(
            cat_id='first_category',
            group_id=Group.objects.get(group_id='first_group')
        )
        Category.objects.create(
            cat_id='second_category',
            group_id=Group.objects.get(group_id='second_group')
        )
        Subcategory.objects.create(
            subcat_id='first_subcat',
            cat_id=Category.objects.get(cat_id='first_category')
        )
        Subcategory.objects.create(
            subcat_id='second_subcat',
            cat_id=Category.objects.get(cat_id='second_category')
        )
        Product.objects.create(
            pr_sku_id='first_product',
            pr_subcat_id=Subcategory.objects.get(subcat_id='first_subcat'),
            pr_uom_id=12
        )
        Product.objects.create(
            pr_sku_id='second_product',
            pr_subcat_id=Subcategory.objects.get(subcat_id='second_subcat'),
            pr_uom_id=22
        )
        Shop.objects.create(
            st_id='first_store',
            st_city_id=City.objects.get(city_id='Moscow'),
            st_division_code_id=Division.objects.get(division_code_id='first_division'),
            st_type_format_id=28,
            st_type_loc_id=56,
            st_type_size_id=42,
            st_is_active=True
        )
        Shop.objects.create(
            st_id='second_store',
            st_city_id=City.objects.get(city_id='Kemerovo'),
            st_division_code_id=Division.objects.get(division_code_id='second_division'),
            st_type_format_id=28,
            st_type_loc_id=56,
            st_type_size_id=42,
            st_is_active=True
        )
        Sale.objects.create(
            st_id=Shop.objects.get(st_id='first_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='first_product'),
            date='2023-05-28',
            pr_sales_type_id=True,
            pr_sales_in_units=10,
            pr_promo_sales_in_units=10,
            pr_sales_in_rub=0,
            pr_promo_sales_in_rub=1000
        )
        Sale.objects.create(
            st_id=Shop.objects.get(st_id='first_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='first_product'),
            date='2023-05-29',
            pr_sales_type_id=False,
            pr_sales_in_units=10,
            pr_promo_sales_in_units=0,
            pr_sales_in_rub=2000,
            pr_promo_sales_in_rub=0
        )
        Sale.objects.create(
            st_id=Shop.objects.get(st_id='second_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='second_product'),
            date='2023-05-28',
            pr_sales_type_id=True,
            pr_sales_in_units=10,
            pr_promo_sales_in_units=10,
            pr_sales_in_rub=0,
            pr_promo_sales_in_rub=1000
        )
        Sale.objects.create(
            st_id=Shop.objects.get(st_id='second_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='second_product'),
            date='2023-05-29',
            pr_sales_type_id=False,
            pr_sales_in_units=10,
            pr_promo_sales_in_units=0,
            pr_sales_in_rub=2000,
            pr_promo_sales_in_rub=0
        )
        Forecast.objects.create(
            st_id=Shop.objects.get(st_id='first_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='first_product'),
            date='2023-07-19',
            target=2,
            calc_date='2023-07-18'
        )
        Forecast.objects.create(
            st_id=Shop.objects.get(st_id='first_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='first_product'),
            date='2023-07-20',
            target=5,
            calc_date='2023-07-18'
        )
        Forecast.objects.create(
            st_id=Shop.objects.get(st_id='first_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='first_product'),
            date='2023-07-21',
            target=7,
            calc_date='2023-07-18'
        )
        Forecast.objects.create(
            st_id=Shop.objects.get(st_id='first_store'),
            pr_sku_id=Product.objects.get(pr_sku_id='first_product'),
            date='2023-07-22',
            target=2,
            calc_date='2023-07-18'
        )

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

    def test_api_v1_cities(self):
        response = self.auth_client.get('/api/v1/cities/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), City.objects.count())

    def test_api_v1_cities_id(self):
        city = City.objects.first()
        response = self.auth_client.get(
            f'/api/v1/cities/{city.id}/'
        )
        self.assertEqual(response.data['city_id'], city.city_id)

    def test_api_v1_divisions(self):
        response = self.auth_client.get('/api/v1/divisions/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Division.objects.count())

    def test_api_v1_divisions_id(self):
        div = Division.objects.first()
        response = self.auth_client.get(f'/api/v1/divisions/{div.id}/')
        self.assertEqual(
            response.data['division_code_id'], div.division_code_id
        )

    def test_api_v1_groups(self):
        response = self.auth_client.get('/api/v1/groups/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Group.objects.count())

    def test_api_v1_groups_id(self):
        group = Group.objects.first()
        response = self.auth_client.get(f'/api/v1/grops/{group.id}/')
        self.assertEqual(response.data['group_id'], group.group_id)

    def test_api_v1_catrgories(self):
        response = self.auth_client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), Category.objects.count())

    def test_api_v1_categories_id(self):
        cat = Category.objects.first()
        response = self.auth_client.get(f'/api/v1/categories/{cat.id}/')
        self.assertEqual(response.data['cat_id'], cat.cat_id)
        self.assertEqual(response.data['group_id'], cat.group_id.id)

    def test_api_v1_products(self):
        response = self.auth_client.get('/api/v1/products/')
        self.assertEqual(response.data['count'], Product.objects.count())
        self.assertTrue(response.data['results'])

    def test_api_v1_products_id(self):
        product = Product.objects.first()
        response = self.auth_client.get(f'/api/v1/products/{product.id}/')
        self.assertEqual(set(response.data.keys()), set(('id', 'sku')))
        self.assertEqual(response.data['sku'], product.pr_sku_id)

    def test_api_v1_shops(self):
        response = self.auth_client.get('/api/v1/shops/')
        self.assertEqual(len(response.data), Shop.objects.count())
        self.assertEqual(
            set(response.data[0].keys()),
            set(
                ('id', 'store', 'city', 'division', 'type_format', 'loc',
                 'size', 'is_active')
            )
        )

    def test_api_v1_shops_id(self):
        shop = Shop.objects.first()
        response = self.auth_client.get(f'/api/v1/shops/{shop.id}/')
        self.assertEqual(response.data['store'], shop.st_id)
        self.assertEqual(
            set(response.data.keys()),
            set(
                ('id', 'store', 'city', 'division', 'type_format', 'loc',
                 'size', 'is_active')
            )
        )

    def test_api_v1_sales(self):
        response = self.auth_client.get('/api/v1/sales/')
        self.assertEqual(response.data['count'], Sale.objects.count())
        self.assertEqual(
            set(response.data['results'][0].keys()),
            set(
                ('st_id', 'pr_sku_id', 'date', 'pr_sales_in_units')
            )
        )

    def test_api_v1_sales_id(self):
        sale = Sale.objects.first()
        response = self.auth_client.get(f'/api/v1/sales/{sale.id}/')
        self.assertEqual(
            set(response.data.keys()),
            set(
                ('st_id', 'pr_sku_id', 'date', 'pr_sales_in_units')
            )
        )
        self.assertEqual(response.data['pr_sku_id'], sale.pr_sku_id.id)

    def test_api_v1_filters_groups_whith_sales(self):
        response = self.auth_client.get(
            '/api/v1/filters/groups_whith_sales/'
        )
        self.assertEqual(len(response.data), Shop.objects.count())
        self.assertEqual(
            set(response.data[0].keys()),
            set(
                ('id', 'st_id', 'groups')
            )
        )
        self.assertEqual(
            set(response.data[0]['groups'][0].keys()),
            set(('id', 'group_id'))
        )
        self.assertTrue(Sale.objects.filter(
            st_id=get_object_or_404(Shop, id=response.data[0]['id']),
            pr_sku_id=get_object_or_404(
                Product,
                pr_subcat_id__cat_id__group_id=response.data[0]['groups'][0]['id']
            )
        ).exists())

    def test_api_v1_filters_categories_with_sales(self):
        path = '/api/v1/filters/categories_with_sales/'
        wrong_query_params = (
            '?',
            '?store=1',
            '?group=1',
        )
        for query in wrong_query_params:
            with self.subTest(query=query):
                response = self.auth_client.get(
                    f'{path}{query}'
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.auth_client.get(
            f'{path}?store=1&group=1'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            set(response.data[0].keys()), set(('groups',))
        )
        self.assertEqual(
            set(response.data[0]['groups'][0].keys()),
            set(('id', 'categories',))
        )
        self.assertEqual(
            response.data[0]['groups'][0]['id'],
            int(response.wsgi_request.GET['group'])
        )
        self.assertEqual(
            set(response.data[0]['groups'][0]['categories'][0].keys()),
            set(('id', 'cat_id', 'group_id',))
        )

    def test_api_v1_filters_subcategories_with_sales(self):
        path = '/api/v1/filters/subcategories_with_sales/'
        wrong_query_params = (
            '?',
            '?store=1',
            '?store=1&group=1',
            '?group=1&category=1'
        )
        for query in wrong_query_params:
            with self.subTest(query=query):
                response = self.auth_client.get(f'{path}{query}')
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.auth_client.get(
            f'{path}?store=1&group=1&category=1'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            set(response.data[0].keys()), set(('categories',))
        )
        self.assertEqual(
            set(response.data[0]['categories'][0].keys()),
            set(('id', 'cat_id', 'group_id', 'subcategories'))
        )
        self.assertEqual(
            set(response.data[0]['categories'][0]['subcategories'][0].keys()),
            set(('id', 'subcat_id', 'cat_id'))
        )

    def test_api_v1_filters_category(self):
        path = '/api/v1/filters/category/'
        wrong_query_params = (
            '?',
            '?store=1',
            '?group=1',
        )
        for query in wrong_query_params:
            with self.subTest(query=query):
                response = self.auth_client.get(
                    f'{path}{query}'
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.auth_client.get(
            f'{path}?store=1&group=1&category=1'
        )
        self.assertEqual(
            set(response.data[0].keys()),
            set(('id', 'cat_id', 'group_id',))
        )

    def test_api_v1_filters_products(self):
        path = '/api/v1/filters/products/'
        wrong_query_params = (
            '?',
            '?store=1',
            '?store=1&group=1',
            '?store=1&group=1&category=1',
            '?group=1&category=1&subcategory=1',
        )
        for query in wrong_query_params:
            with self.subTest(query=query):
                response = self.auth_client.get(
                    f'{path}{query}'
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.auth_client.get(
            f'{path}?store=1&group=1&category=1&subcategory=1'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            set(response.data[0].keys()), set(('id', 'pr_sku_id'))
        )

    def test_api_v1_forecast_get_forecast(self):
        path = '/api/v1/forecast/get_forecast/'
        wrong_query_params = (
            '?',
            '?store=1',
            '?product=1'
        )
        for query in wrong_query_params:
            with self.subTest(query=query):
                response = self.auth_client.get(
                    f'{path}{query}'
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.auth_client.get(
            f'{path}?store=1&product=1'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            set(response.data[0].keys()),
            set(('id', 'st_id', 'product'))
        )
        self.assertEqual(
            set(response.data[0]['product'].keys()),
            set(('id', 'pr_sku_id', 'pr_uom_id', 'predict'))
        )
        self.assertEqual(
            set(response.data[0]['product']['predict'][0].keys()),
            set(('date', 'target'))
        )

    def test_api_v1_get_sales(self):
        path = '/api/v1/get_sales/'
        wrong_query_params = (
            '?',
            '?store=1',
            '?sku=1'
        )
        for query in wrong_query_params:
            with self.subTest(query=query):
                response = self.auth_client.get(
                    f'{path}{query}'
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.auth_client.get(
            f'{path}?store=1&sku=1'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            set(response.data[0].keys()),
            set(('date', 'pr_sales_in_units',))
        )
