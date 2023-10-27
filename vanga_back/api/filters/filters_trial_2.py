from rest_framework import filters
from rest_framework.exceptions import ValidationError


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
