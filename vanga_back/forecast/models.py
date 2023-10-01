from django.db import models

from backend.models import Shop, Product


class BaseForecast(models.Model):
    """Базовая модель прогноза"""
    st_id = models.ForeignKey(Shop,
                              on_delete=models.CASCADE,
                              related_name='fc_stores')
    pr_sku_id = models.ForeignKey(Product,
                                  on_delete=models.CASCADE,
                                  related_name='fc_products')
    date = models.DateField('Дата')
    target = models.IntegerField('Прогноз продаж')

    class Meta:
        abstract = True


class Forecast(BaseForecast):
    """Прогноз, сделанный в определенную дату"""
    calc_date = models.DateField('Дата расчета прогноза')

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'
        ordering = ['-date']
