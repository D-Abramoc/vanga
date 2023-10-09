from rest_framework import viewsets, serializers
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from backend.models import Sale


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
        # OpenApiParameter(
        #     'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
        #     required=True
        # ),
        # OpenApiParameter(
        #     'category', OpenApiTypes.INT, OpenApiParameter.QUERY,
        #     required=True
        # ),
        # OpenApiParameter(
        #     'subcategory', OpenApiTypes.INT, OpenApiParameter.QUERY,
        #     required=True
        # ),
        OpenApiParameter(
            'sku', OpenApiTypes.INT, OpenApiParameter.QUERY,
            required=True
        ),
        # OpenApiParameter(
        #     'start', OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
        #     required=True
        # ),
        # OpenApiParameter(
        #     'end', OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
        #     required=True
        # )
        ]
    )
)
class NewSalesViewSet(viewsets.ModelViewSet):
    # queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_queryset(self):
        return (
            Sale.objects.filter(
                st_id=self.request.query_params['store'],
                pr_sales_type_id=False,
                # pr_sku_id__pr_subcat_id__cat_id__group_id=self.request.query_params['group'],
                # pr_sku_id__pr_subcat_id__cat_id=self.request.query_params['category'],
                # pr_sku_id__pr_subcat_id=self.request.query_params['subcategory'],
                pr_sku_id=self.request.query_params['sku'],
                # date__range=[
                #     self.request.query_params['start'],
                #     self.request.query_params['end']
                # ]
            )
        )
