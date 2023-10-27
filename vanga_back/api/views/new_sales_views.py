from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError

from backend.models import Sale
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('date', 'pr_sales_in_units')


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'sku', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
        ]
    )
)
class NewSalesViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer

    def get_queryset(self):
        if ('store' not in self.request.query_params
                or 'sku' not in self.request.query_params):
            raise ValidationError('Проверьте обязательные параметры: '
                                  'store, sku')
        return (
            Sale.objects.filter(
                st_id=self.request.query_params['store'],
                pr_sales_type_id=False,
                pr_sku_id=self.request.query_params['sku'],
            )
        )
