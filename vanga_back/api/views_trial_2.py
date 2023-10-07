from rest_framework import viewsets
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter,)
from drf_spectacular.types import OpenApiTypes

from backend.models import Shop
from .serializers_trial_2 import (GroupWithSalesSerializer,
                                  CategoriesWithSalesSerializer,
                                  SubcategoriesWithSalesSerializer)
from .filters_trial_2 import ShopFilter


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
