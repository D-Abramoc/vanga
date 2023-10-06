from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter,)
from drf_spectacular.types import OpenApiTypes

from backend.models import Shop, Group
from .serializers_trial_2 import (GroupWithSalesSerializer,
                                  CategoriesWithSalesSerializer,
                                  SubcategoriesWithSalesSerializer)
from .filters_trial_2 import ShopFilter, GroupFilter


@extend_schema_view(
    list=extend_schema(
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


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY
            )
        ]
    )
)
class CategoriesWithSalesInShop(viewsets.ModelViewSet):
    serializer_class = CategoriesWithSalesSerializer
    queryset = Shop.objects.all()
    filter_backends = (ShopFilter, )


@extend_schema_view(
    list=extend_schema(
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
