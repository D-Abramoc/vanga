
from backend.models import (Category, City, Division, Group, Product,
                            Sale, Shop)
from forecast.models import Forecast
from djoser import views
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   OpenApiParameter,)
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .paginators import MaxLimitLimitOffsetPagination
from .serializers import (CategorySerializer, CitySerializer,
                          DivisionSerializer, ForecastSerializer,
                          ProductSerializer, SaleSerializer,
                          ShopSerializer, MeUserSerializer,
                          TestGroupSerializer,)
from .serializers_trial import StoreProductPeriodSerializer
from .utils import get_query_params


# @extend_schema(tags=['Продажи'])
# @extend_schema_view(
#     list=extend_schema(
#         summary='Получить продажи определённого товара за период',
#         parameters=[
#             OpenApiParameter(
#                 'start_date', OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
#                 default='2023-05-28'
#             ),
#             OpenApiParameter(
#                 'end_date', OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
#                 default='2023-06-28'
#             ),
#             OpenApiParameter(
#                 'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
#                 default=6
#             ),
#             OpenApiParameter(
#                 'sku', OpenApiTypes.INT, OpenApiParameter.QUERY, default=1186
#             ),
#         ]
#     )
# )
# class GetProductSalesForPeriod(viewsets.ModelViewSet):
#     '''
#     Возвращает данные о продажах выбранного товара.

#     На вход получает товар, магазин, дату от которой смотрим
#     и количество дней на сколько смотрим.
#     '''
#     queryset = Sale.objects.all()
#     serializer_class = SaleSerializer
#     filter_backends = (DateFilter, StoreFilter, SKUFilter)
#     pagination_class = MaxLimitLimitOffsetPagination


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


@extend_schema(tags=['Пользователь'])
@extend_schema_view(
    post=extend_schema(
        summary='Обновить токен'
    )
)
class RefreshTokenViewSet(TokenRefreshView):
    '''Обновление access token'''
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
    pagination_class = MaxLimitLimitOffsetPagination
    http_method_names = ('get', 'post')


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
    serializer_class = TestGroupSerializer


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


@extend_schema(
        tags=['Продажи'],
        summary='Получить продажи за период по паре магазин-товар',
        description='''Все поля пока обязательные, но если успею добавлю
        гибкости. Магазины и товары выбираются по id. Можно выбирать по
        несколько, но без фанатизма.
        ''',
        parameters=[
            OpenApiParameter(
                'start_date', OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
                default='2023-05-28', required=False
            ),
            OpenApiParameter(
                'time_delta', OpenApiTypes.INT, OpenApiParameter.QUERY,
                default=14, required=False
            ),
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                default=6, required=False
            ),
            OpenApiParameter(
                'sku', OpenApiTypes.INT, OpenApiParameter.QUERY,
                default=1186, required=False
            ),
        ]
)
class GetSalesViewSet(viewsets.ModelViewSet):
    serializer_class = StoreProductPeriodSerializer

    def get_queryset(self):
        if 'store' not in self.request.query_params:
            raise serializers.ValidationError('An ass happend!')
        request_query_params = get_query_params(self.request.query_params)
        return Shop.objects.filter(id__in=request_query_params['store'])
# @api_view(['GET'])
# def get_sales(request):
#     if not request.query_params:
#         return Response('При запросе без фильтров всё упадёт.')
#     rqps = [
#         (key, request.query_params.getlist(key))
#         for key in request.query_params
#     ]
#     qps = dict(rqps)
#     queryset = Shop.objects.filter(id__in=qps['store'])
#     serializer = TSerializer(queryset, many=True, context={'query': qps})
#     return Response(serializer.data, status.HTTP_200_OK)
