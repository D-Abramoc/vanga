from rest_framework import filters


class TestFilter(filters.BaseFilterBackend):
    # def __init__(self, request, queryset) -> None:
    #     super().__init__()

    def filter_queryset(self, request, queryset, view):
        return queryset


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
