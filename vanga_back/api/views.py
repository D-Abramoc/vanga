from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from djoser import views

import pandas as pd
from backend.models import Category, City, Division, Group, Product, Sale, Shop
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema,
                                   extend_schema_view)
from forecast.models import Forecast
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .paginators import MaxLimitLimitOffsetPagination
from .serializers import (CategorySerializer, CitySerializer,
                          DivisionSerializer, ForecastSerializer,
                          GroupSerializer, MeUserSerializer, ProductSerializer,
                          SaleSerializer, ShopSerializer, TestGroupSerializer)
from .serializers_trial import StoreProductPeriodSerializer
from .utils import get_query_params


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

    @action(detail=False, methods=['get'],
            url_name='download_forecast',
            url_path='download_forecast')
    def download_forecast(self, request):
        filetype = request.query_params['filetype']
        st_id = request.query_params['st_id']
        pr_sku_id = request.query_params['pr_sku_id']

        if filetype not in ['xlsx', 'csv']:
            return HttpResponse('Неподдерживаемый формат файла', status=400)

        shop = get_object_or_404(Shop, id=st_id)
        product = get_object_or_404(Product, id=pr_sku_id)
        forecast_items = Forecast.objects.filter(st_id=shop,
                                                 pr_sku_id=product)

        forecast_list = []
        for forecast in forecast_items:
            forecast_list.append([forecast.st_id,
                                  forecast.pr_sku_id,
                                  forecast.date,
                                  forecast.target])
        forecast_df = pd.DataFrame(forecast_list)

        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            forecast_df.to_excel(writer, index=False, header=False)
            writer.close()
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="forecast.{filetype}"'

        return response


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
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=['post'],
            url_name='upload',
            url_path='upload')
    def upload(self, request):
        if len(request.FILES) != 1:
            return HttpResponse('Вложите один файл для импорта', status=400)
        file = next(request.FILES.values())
        df = pd.read_csv(file)

        sales = []
        try:
            for index, row in df.iterrows():
                sales.append(Sale(
                    st_id=Shop.objects.get(st_id=row['st_id']),
                    pr_sku_id=Product.objects.get(pr_sku_id=row['pr_sku_id']),
                    date=row['date'],
                    pr_sales_type_id=row['pr_sales_type_id'],
                    pr_sales_in_units=row['pr_sales_in_units'],
                    pr_promo_sales_in_units=row['pr_promo_sales_in_units'],
                    pr_sales_in_rub=row['pr_sales_in_rub'],
                    pr_promo_sales_in_rub=row['pr_promo_sales_in_rub'])
                )
        except KeyError:
            return HttpResponse('Неверный формат столбцов', status=201)
        Sale.objects.bulk_create(sales)

        return HttpResponse('Импорт продаж завершен', status=201)


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


@extend_schema(
    tags=['Продажи'])
@extend_schema_view(
    list=extend_schema(
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
        ],
        # external_docs={
        #     'a': 'b'
        # }
    )
)
class GetSalesViewSet(viewsets.ModelViewSet):
    serializer_class = StoreProductPeriodSerializer

    def get_queryset(self):
        if 'store' not in self.request.query_params:
            raise serializers.ValidationError('An ass happend!')
        request_query_params: dict[str, list[str] | str] = (
            get_query_params(self.request.query_params)
        )
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
