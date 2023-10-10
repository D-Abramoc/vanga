from rest_framework import viewsets

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from forecast.models import Forecast

from .filter_forecast import ForecastByShopFilter
from .serializers_forecast import ForecastSerializer


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
