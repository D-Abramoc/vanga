from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from backend.models import (City, Product, Shop, Forecast, Sale, Category,
                            Group, Division)

from .serializers import (CitySerializer, ProductSerializer, ShopSerializer,
                          ForecastSerializer, SaleSerializer,
                          CategorySerializer, GroupSerializer,
                          DivisionSerializer)


@extend_schema(tags=['Прогноз'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить прогноз'
    )
)
class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer


@extend_schema(tags=['Продажи'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список продаж'
    )
)
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


@extend_schema(tags=['Категории'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список категорий'
    )
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=['Группы товаров'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить группы товаров'
    )
)
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@extend_schema(tags=['Дивизионы'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список дивизионов'
    )
)
class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


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
@extend_schema_view(
    list=extend_schema(
        summary='Получить список товаров'
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(tags=['Города присутствия'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список городов'
    )
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
