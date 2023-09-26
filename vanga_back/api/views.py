from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from backend.models import City, Product, Shop

from .serializers import ProductSerializer, ShopSerializer


@extend_schema(tags=['Список ТЦ'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список ТЦ'
    )
)
class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


@extend_schema(tags=['Товарная иерархия'])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
