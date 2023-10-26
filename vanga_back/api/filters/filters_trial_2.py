from rest_framework import filters
from rest_framework.exceptions import ValidationError

from backend import models as m


class ShopFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'store' not in request.query_params:
            raise ValidationError('store is required parameter.')
        return queryset.filter(id=request.query_params['store'])


class GroupFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'group' not in request.query_params:
            raise ValidationError('group is required parameter.')
        return queryset
