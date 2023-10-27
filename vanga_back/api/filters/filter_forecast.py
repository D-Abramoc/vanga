from rest_framework import filters
from rest_framework.exceptions import ValidationError


class ForecastByShopFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if (('store' not in request.query_params)
                or 'product' not in request.query_params):
            raise ValidationError('Проверьте, что переданы обязательные '
                                  'параметры: store и product')
        res = queryset.filter(st_id=request.query_params['store'],
                              pr_sku_id=request.query_params['product'])
        return res.distinct('pr_sku_id')
