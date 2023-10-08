from django.test import TestCase

import backend.models as m


class BackendModelTest(TestCase):
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

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        city = BackendModelTest.city
        division = BackendModelTest.division
        shop = BackendModelTest.shop
        group = BackendModelTest.group
        category = BackendModelTest.category
        subcategory = BackendModelTest.subcategory
        product = BackendModelTest.product
        sale = BackendModelTest.sale

        expected_str_values = {
            city: 'city0000000000000000000000000001',
            division: 'division000000000000000000000001',
            shop: 'shop0000000000000000000000000001',
            group: 'group000000000000000000000000001',
            category: 'categoty000000000000000000000001',
            subcategory: 'subcategoty000000000000000000001',
            product: 'product0000000000000000000000001',
            sale: 'Продано единиц товара product0000000000000000000000001: 1',
        }

        for model, expected_value in expected_str_values.items():
            with self.subTest(model=model):
                self.assertEqual(str(model), expected_value)

    def test_models_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        city = BackendModelTest.city
        division = BackendModelTest.division
        shop = BackendModelTest.shop
        group = BackendModelTest.group
        category = BackendModelTest.category
        subcategory = BackendModelTest.subcategory
        product = BackendModelTest.product
        sale = BackendModelTest.sale

        field_verbose = {
            city: {'city_id': 'Хэш id города'},
            division: {'division_code_id': 'Хэш id дивизиона'},
            shop: {'st_id': 'Хэш id магазина',
                   'st_type_format_id': 'id формата магазина',
                   'st_type_loc_id': 'id/тип локации/окружения магазина',
                   'st_type_size_id': 'id типа размера магазина',
                   'st_is_active': 'Флаг активного магазина'},
            group: {'group_id': 'Хэш id группы товаров'},
            category: {'cat_id': 'Хэш id категории товаров'},
            subcategory: {'subcat_id': 'Хэш id подкатегории товаров'},
            product: {'pr_sku_id': 'Хэш id товара',
                      'pr_uom_id': 'Код единиц измерения товара'},
            sale: {'date': 'Дата',
                   'pr_sales_type_id': 'Флаг наличия промо',
                   'pr_sales_in_units': 'Продано товаров',
                   'pr_promo_sales_in_units': 'Продано товаров с промо',
                   'pr_sales_in_rub': 'Продажи без промо, руб',
                   'pr_promo_sales_in_rub': 'Продажи с промо, руб'},
        }

        for model in field_verbose:
            for field, expected_value in field_verbose[model].items():
                with self.subTest(field=field):
                    self.assertEqual(
                        model._meta.get_field(field).verbose_name, expected_value)

    def test_sale_to_dict_method(self):
        """Метод to_dict модели Sale отдает ожидаемые значения"""
        sale = BackendModelTest.sale
        expected_dict = {
            'st_id': 'shop0000000000000000000000000001',
            'pr_sku_id': 'product0000000000000000000000001',
            'date': '2023-07-18',
            'pr_sales_type_id': '1',
            'pr_sales_in_units': '1',
            'pr_promo_sales_in_units': '1',
            'pr_sales_in_rub': '1',
            'pr_promo_sales_in_rub': '1',
        }
        self.assertEqual(sale.to_dict(), expected_dict)
