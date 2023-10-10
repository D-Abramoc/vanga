from django.test import TestCase

import backend.models as m
from forecast.functions import save_forecast
from forecast.models import Forecast


class ForecastModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = m.City.objects.create(
            city_id='city0000000000000000000000000001'
        )
        cls.division = m.Division.objects.create(
            division_code_id='division000000000000000000000001'
        )
        cls.shop = m.Shop.objects.create(
            st_id='shop0000000000000000000000000001',
            st_city_id=cls.city,
            st_division_code_id=cls.division,
            st_type_format_id=1,
            st_type_loc_id=1,
            st_type_size_id=1,
            st_is_active=1
        )
        cls.group = m.Group.objects.create(
            group_id='group000000000000000000000000001'
        )
        cls.category = m.Category.objects.create(
            group_id=cls.group,
            cat_id='categoty000000000000000000000001'
        )
        cls.subcategory = m.Subcategory.objects.create(
            cat_id=cls.category,
            subcat_id='subcategoty000000000000000000001'
        )
        cls.product = m.Product.objects.create(
            pr_sku_id='product0000000000000000000000001',
            pr_subcat_id=cls.subcategory,
            pr_uom_id='17'
        )
        cls.sale = m.Sale.objects.create(
            st_id=cls.shop,
            pr_sku_id=cls.product,
            date='2023-07-18',
            pr_sales_type_id=1,
            pr_sales_in_units=1,
            pr_promo_sales_in_units=1,
            pr_sales_in_rub=1,
            pr_promo_sales_in_rub=1
        )

    def test_save_forecast_creates_forecasts(self):
        """Проверяем, что функция get_forecast сохраняет прогноз"""
        fc_json: list[dict] = [
            {'st_id': 'shop0000000000000000000000000001',
             'pr_sku_id': 'product0000000000000000000000001',
             'date': '2023-07-19',
             'target': 5},
            {'st_id': 'shop0000000000000000000000000001',
             'pr_sku_id': 'product0000000000000000000000001',
             'date': '2023-07-20',
             'target': 5}
        ]
        save_forecast(fc_json)
        self.assertEqual(Forecast.objects.all().count(), 2)
