# from filters
from rest_framework import filters

# from filters_trial
from rest_framework.exceptions import ValidationError


# from filters_forecast
class ForecastByShopFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if (('store' not in request.query_params)
                or 'product' not in request.query_params):
            raise ValidationError('Проверьте, что переданы обязательные '
                                  'параметры: store и product')
        res = queryset.filter(st_id=request.query_params['store'],
                              pr_sku_id=request.query_params['product'])
        return res.distinct('pr_sku_id')


# from filters_trial
class ShopFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'store' not in request.query_params:
            raise ValidationError('store is required parameter.')
        return queryset.filter(id=request.query_params['store'])


class GroupFilterForValidate(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'group' not in request.query_params:
            raise ValidationError('group is required parameter.')
        return queryset


class CategoryFilterForValidate(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'category' not in request.query_params:
            raise ValidationError('category is required parameter.')
        return queryset


# from filter
class DateFilter(filters.BaseFilterBackend):
    '''Фильтр по датам.'''

    def filter_queryset(self, request, queryset, view):
        if 'start_date' not in request.query_params:
            return queryset
        if 'end_date' not in request.query_params:
            return queryset.filter(date=request.query_params.get('start_date'))
        return queryset.filter(
            date__range=[request.query_params.get('start_date'),
                         request.query_params.get('end_date')]
        )


class StoreFilter(filters.BaseFilterBackend):
    '''Фильтр по ТЦ.'''

    def filter_queryset(self, request, queryset, view):
        if 'store' not in request.query_params:
            return queryset
        rqps = [
            (key, request.query_params.getlist(key))
            for key in request.query_params
        ]
        qps = dict(rqps)
        return queryset.filter(
            id__in=qps.get('store')
        )


class SKUFilter(filters.BaseFilterBackend):
    '''Фильтр по товару.'''

    def filter_queryset(self, request, queryset, view):
        if 'sku' not in request.query_params:
            return queryset
        return queryset.filter(pr_sku_id__in=request.query_params.get('sku'))
