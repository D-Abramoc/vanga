from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError

from backend.models import Category, Product, Shop

from ..filters.filters_trial_2 import ShopFilter
from ..serializers.serializers_category import CategorySerialiser
from ..serializers.serializers_product import ProductSerialiser
from ..serializers.serializers_trial_2 import (
    CategoriesWithSalesSerializer, GroupWithSalesSerializer,
    SubcategoriesWithSalesSerializer)


class ProductFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if ('store' not in request.query_params
                or 'group' not in request.query_params
                or 'category' not in request.query_params
                or 'subcategory' not in request.query_params):
            raise ValidationError('An ass happen')
        res = (
            queryset.filter(
                sales__st_id=(request.query_params['store']),
                pr_subcat_id__cat_id__group_id=request.query_params['group'],
                pr_subcat_id=request.query_params['subcategory'],
                pr_subcat_id__cat_id=request.query_params['category'],
                sales__pr_sales_type_id=False
            )
        )
        return res.distinct('pr_sku_id')


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=12
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=1
            ),
            OpenApiParameter(
                'category', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=9
            ),
            OpenApiParameter(
                'subcategory', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=33
            ),
        ]
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerialiser
    queryset = Product.objects.all()
    filter_backends = (ProductFilter,)


class CategoryFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if ('store' not in request.query_params
                or 'group' not in request.query_params):
            raise ValidationError('An ass happen')
        res = (
            queryset.filter(
                subcategories__products__sales__st_id=(
                    request.query_params['store']
                ),
                group_id=request.query_params['group'],
                subcategories__products__sales__pr_sales_in_units__gt=0,
                subcategories__products__sales__pr_sales_type_id=False
            )
        )
        return res.distinct('cat_id')


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=1
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=2
            )
        ]
    )
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerialiser
    queryset = Category.objects.all()
    filter_backends = (CategoryFilter,)


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить группы',
        description='Возвращает группы в которых были продажи товаров.',
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY
            )
        ]
    )
)
class GroupsWithSalesInShop(viewsets.ModelViewSet):
    serializer_class = GroupWithSalesSerializer
    queryset = Shop.objects.all()
    filter_backends = (ShopFilter,)


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить категории.',
        description=('Возвращает категории в которых были продажи. '
                     'id магазина обязательный параметр'),
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            )
        ]
    )
)
class CategoriesWithSalesInShop(viewsets.ModelViewSet):
    serializer_class = CategoriesWithSalesSerializer
    queryset = Shop.objects.all()
    filter_backends = (ShopFilter, )


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить подкатегории',
        description='Возвращает подкатегории, в которых были продажи',
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'category', OpenApiTypes.INT, OpenApiParameter.QUERY
            )
        ]
    )
)
class SubcategoriesWithSalesInShop(viewsets.ModelViewSet):
    serializer_class = SubcategoriesWithSalesSerializer
    queryset = Shop.objects.all()
    filter_backends = (ShopFilter,)
