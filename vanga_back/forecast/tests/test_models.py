from django.test import TestCase

import backend.models as m
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
        cls.forecast = Forecast.objects.create(
            calc_date='2023-07-18',
            st_id=cls.shop,
            pr_sku_id=cls.product,
            date='2023-07-19',
            target=1,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        forecast = ForecastModelTest.forecast

        self.assertEqual(
            str(forecast),
            'Товар: product0000000000000000000000001, Прогноз: 1'
        )

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        forecast = ForecastModelTest.forecast

        field_verbose = {'date': 'Дата',
                         'target': 'Прогноз продаж',
                         'calc_date': 'Дата расчета прогноза'}

        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    forecast._meta.get_field(field).verbose_name, expected_value)
