from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter)
from drf_spectacular.types import OpenApiTypes

from .serializers import ProductSerialiser

from backend.models import Product


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