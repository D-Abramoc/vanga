from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError

from backend.models import Category
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)

from .serializers import CategorySerialiser


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
