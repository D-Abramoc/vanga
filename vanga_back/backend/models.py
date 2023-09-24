from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .constants import *


class City(models.Model):
    """Модель города"""
    city_id = models.CharField('Хэш id города',
                                  max_length=MAX_HASH_LEN,
                                  unique=True)

    class Meta:
        verbose_name = 'Хэш id города'
        verbose_name_plural = 'Хэш id городов'
        ordering = ['city_id']


class Division(models.Model):
    """Модель дивизиона"""
    division_code_id = models.CharField('Хэш id дивизиона',
                                           max_length=MAX_HASH_LEN,
                                           unique=True)

    class Meta:
        verbose_name = 'Хэш id дивизиона'
        verbose_name_plural = 'Хэш id дивизионов'
        ordering = ['division_code_id']


class Shop(models.Model):
    """Модель магазина"""
    st_id = models.CharField('Хэш id магазина',
                             max_length=MAX_HASH_LEN,
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
                MIN_SIZE_ID, message='Минимальное значение: 1'),
            MaxValueValidator(
                MAX_SIZE_ID, message='Максимальное значение: 100')
        ]
    )
    st_is_active = models.BooleanField('Флаг активного магазина')

    class Meta:
        verbose_name = 'Хэш id магазина'
        verbose_name_plural = 'Хэш id магазинов'
        ordering = ['st_id']


class Group(models.Model):
    """Модель группы товаров"""
    group_id = models.CharField('Хэш id группы товаров',
                                   max_length=MAX_HASH_LEN,
                                   unique=True)

    class Meta:
        verbose_name = 'Хэш id группы товаров'
        verbose_name_plural = 'Хэш id групп товаров'
        ordering = ['group_id']


class Category(models.Model):
    """Модель категории товаров"""
    group_id = models.ForeignKey(Group,
                                 on_delete=models.CASCADE,
                                 related_name='groups')
    cat_id = models.CharField('Хэш id категории товаров',
                              max_length=MAX_HASH_LEN,
                              unique=True)

    class Meta:
        verbose_name = 'Хэш id категории товаров'
        verbose_name_plural = 'Хэш id категорий товаров'
        ordering = ['cat_id']


class Subcategory(models.Model):
    """Модель подкатегории товаров"""
    cat_id = models.ForeignKey(Category,
                               on_delete=models.CASCADE,
                               related_name='categories')
    subcat_id = models.CharField('Хэш id подкатегории товаров',
                                    max_length=MAX_HASH_LEN,
                                    unique=True)

    class Meta:
        verbose_name = 'Хэш id подкатегории товаров'
        verbose_name_plural = 'Хэш id подкатегорий товаров'
        ordering = ['subcat_id']


class Product(models.Model):
    """Модель товара"""
    pr_sku_id = models.CharField('Хэш id товара',
                                 max_length=MAX_HASH_LEN,
                                 unique=True)
    pr_subcat_id = models.ForeignKey(Subcategory,
                                     on_delete=models.CASCADE,
                                     related_name='subcategories')
    pr_uom_id = models.BooleanField('Весовой/штучный товар')

    class Meta:
        verbose_name = 'Хэш id товара'
        verbose_name_plural = 'Хэш id товаров'
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

