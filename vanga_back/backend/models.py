from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import constants as csnt


class City(models.Model):
    """Модель города"""
    city_id = models.CharField('Хэш id города',
                               max_length=csnt.MAX_HASH_LEN,
                               unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['city_id']


class Division(models.Model):
    """Модель дивизиона"""
    division_code_id = models.CharField('Хэш id дивизиона',
                                        max_length=csnt.MAX_HASH_LEN,
                                        unique=True)

    class Meta:
        verbose_name = 'Дивизион'
        verbose_name_plural = 'Дивизионы'
        ordering = ['division_code_id']


class Shop(models.Model):
    """Модель магазина"""
    st_id = models.CharField('Хэш id магазина',
                             max_length=csnt.MAX_HASH_LEN,
                             unique=True)
    st_city_id = models.ForeignKey(City,
                                   on_delete=models.CASCADE,
                                   related_name='cities',
                                   verbose_name='Хэш id города')
    st_division_code_id = models.ForeignKey(Division,
                                            on_delete=models.CASCADE,
                                            related_name='divisions',
                                            verbose_name='Хэш id дивизиона')
    st_type_format_id = models.IntegerField('id формата магазина')
    st_type_loc_id = models.IntegerField('id/тип локации/окружения магазина')
    st_type_size_id = models.IntegerField(
        'id типа размера магазина',
        validators=[
            MinValueValidator(
                csnt.MIN_SIZE_ID, message='Минимальное значение: 1'),
            MaxValueValidator(
                csnt.MAX_SIZE_ID, message='Максимальное значение: 100')
        ]
    )
    st_is_active = models.BooleanField('Флаг активного магазина')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['st_id']


class Group(models.Model):
    """Модель группы товаров"""
    group_id = models.CharField('Хэш id группы товаров',
                                max_length=csnt.MAX_HASH_LEN,
                                unique=True)

    class Meta:
        verbose_name = 'Группа товаров'
        verbose_name_plural = 'Группы товаров'
        ordering = ['group_id']


class Category(models.Model):
    """Модель категории товаров"""
    group_id = models.ForeignKey(Group,
                                 on_delete=models.CASCADE,
                                 related_name='groups')
    cat_id = models.CharField('Хэш id категории товаров',
                              max_length=csnt.MAX_HASH_LEN,
                              unique=True)

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'
        ordering = ['cat_id']


class Subcategory(models.Model):
    """Модель подкатегории товаров"""
    cat_id = models.ForeignKey(Category,
                               on_delete=models.CASCADE,
                               related_name='categories')
    subcat_id = models.CharField('Хэш id подкатегории товаров',
                                 max_length=csnt.MAX_HASH_LEN,
                                 unique=True)

    class Meta:
        verbose_name = 'Подкатегория товаров'
        verbose_name_plural = 'Подкатегории товаров'
        ordering = ['subcat_id']


class Product(models.Model):
    """Модель товара"""
    pr_sku_id = models.CharField('Хэш id товара',
                                 max_length=csnt.MAX_HASH_LEN,
                                 unique=True)
    pr_subcat_id = models.ForeignKey(Subcategory,
                                     on_delete=models.CASCADE,
                                     related_name='subcategories')
    pr_uom_id = models.IntegerField('Код единиц измерения товара')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['pr_sku_id']


class Sale(models.Model):
    """Модель продажи"""
    st_id = models.ForeignKey(Shop,
                              on_delete=models.CASCADE,
                              related_name='stores')
    pr_sku_id = models.ForeignKey(Product,
                                  on_delete=models.CASCADE,
                                  related_name='products')
    date = models.DateField('Дата')
    pr_sales_type_id = models.BooleanField('Флаг наличия промо')
    pr_sales_in_units = models.IntegerField('Продано товаров')
    pr_promo_sales_in_units = models.IntegerField('Продано товаров с промо')
    pr_sales_in_rub = models.IntegerField('Продажи без промо, руб')
    pr_promo_sales_in_rub = models.IntegerField('Продажи с промо, руб')

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        ordering = ['-date']
