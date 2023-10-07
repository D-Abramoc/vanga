from rest_framework import viewsets
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter)
from drf_spectacular.types import OpenApiTypes

from forecast.models import Forecast

from .serializers_forecast import ForecastSerializer
from .filter_forecast import ForecastByShopFilter


@extend_schema_view(
    list=extend_schema(
        summary='Прогноз по паре магазин-товар',
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=5
            ),
            OpenApiParameter(
                'product', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=1308
            )
        ]
    )
)
class ForecastViewSet(viewsets.ModelViewSet):
    serializer_class = ForecastSerializer
    queryset = Forecast.objects.all()
    filter_backends = (ForecastByShopFilter,)

    def get_queryset(self):
        res = super().get_queryset()
        return res
