from rest_framework import filters

from backend import models as m


class ShopFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'store' not in request.query_params:
            return queryset
        return queryset.filter(id=request.query_params['store'])


class GroupFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'group' not in request.query_params:
            return queryset
        shop = m.Shop.objects.get(id=request.query_params['store'])
        group = request.query_params['group']
        sales = m.Sale.objects.filter(st_id=shop, pr_sales_type_id=False)
        products = m.Product.objects.filter(sales__in=sales)
        subcategories = m.Subcategory.objects.filter(products__in=products)
        categories = m.Category.objects.filter(subcategories__in=subcategories)
        queryset = (
            m.Group.objects.filter(categories__in=categories)
            .distinct().order_by('id')
        )
        return queryset.filter(id=group)
