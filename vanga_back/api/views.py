from backend.models import (Category, City, Division, Group, Product,
                            Sale, Shop)
from forecast.models import Forecast
from djoser import views
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter,)
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .custom_paginators import MaxLimitLimitOffsetPagination
from .filters import DateFilter, StoreFilter, SKUFilter
from .serializers import (CategorySerializer, CitySerializer,
                          DivisionSerializer, ForecastSerializer,
                          GroupSerializer, ProductSerializer, SaleSerializer,
                          ShopSerializer, MeUserSerializer)


@extend_schema(tags=['Продажи'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить продажи определённого товара за период',
        parameters=[
            OpenApiParameter(
                'start_date', OpenApiTypes.DATETIME, OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                'end_date', OpenApiTypes.DATETIME, OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                'sku', OpenApiTypes.INT, OpenApiParameter.QUERY
            ),
        ]
    )
)
class GetProductSalesForPeriod(viewsets.ModelViewSet):
    '''
    Возвращает данные о продажах выбранного товара.

    На вход получает товар, магазин, дату от которой смотрим
    и количество дней на сколько смотрим.
    '''
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = (DateFilter, StoreFilter, SKUFilter)
    pagination_class = MaxLimitLimitOffsetPagination


@extend_schema(tags=['Пользователь'])
@extend_schema_view(
    me=extend_schema(
        summary='Данные текущего пользователя'
    )
)
class MeUserViewSet(views.UserViewSet):
    '''Данные текущего пользователя.'''
    serializer_class = MeUserSerializer


@extend_schema(tags=['Пользователь'])
@extend_schema_view(
    create=(extend_schema(
        summary='Регистрация пользователя'
    ))
)
class CustomUserViewSet(views.UserViewSet):
    '''Регистрация нового пользователя.'''
    pass


@extend_schema(tags=['Пользователь'])
@extend_schema_view(
    post=extend_schema(
        summary='Создать токен'
    )
)
class CustomTokenViewSet(TokenObtainPairView):
    '''Получение токена аутентификации пользователя.'''
    pass


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
    pagination_class = MaxLimitLimitOffsetPagination


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
    # pagination_class = MaxLimitLimitOffsetPagination


@extend_schema(tags=['Города присутствия'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список городов'
    )
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
