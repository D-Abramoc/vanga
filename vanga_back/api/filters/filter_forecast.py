from rest_framework import filters


class ForecastByShopFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        res = queryset.filter(st_id=request.query_params['store'],
                              pr_sku_id=request.query_params['product'])
        return res.distinct('pr_sku_id')
