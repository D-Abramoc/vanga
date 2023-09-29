from rest_framework import filters


class ShopFilter(filters.BaseFilterBackend):
    '''Фильтр по магазинам'''

    def filter_queryset(self, request, queryset, view):
        if 'store' not in request.query_params:
            return queryset
        return super().filter_queryset(request, queryset, view)
