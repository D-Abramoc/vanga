from rest_framework import filters

from backend import models as m


class ShopFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'store' not in request.query_params:
            return queryset
        return queryset.filter(id=request.query_params['store'])
