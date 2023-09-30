from django.db.models import Count
from rest_framework import filters


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
        return queryset.filter(st_id=request.query_params.get('store'))


class SKUFilter(filters.BaseFilterBackend):
    '''Фильтр по товару.'''

    def filter_queryset(self, request, queryset, view):
        if 'sku' not in request.query_params:
            # return queryset.values('pr_sku_id').annotate(goods=Count('pr_sku_id'))
            return queryset
        return queryset.filter(pr_sku_id=request.query_params.get('sku'))
