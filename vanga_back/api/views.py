from http import HTTPStatus
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.decorators import action

import pandas as pd
from backend.models import Category, City, Division, Group, Product, Sale, Shop
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiParameter, extend_schema,
                                   extend_schema_view)
from forecast.models import Forecast

from .paginators import MaxLimitLimitOffsetPagination
from .serializers import (CategorySerializer, CitySerializer,
                          DivisionSerializer, ForecastSerializer,
                          GroupSerializer, ProductSerializer,
                          SaleSerializer, ShopSerializer)
from .serializers import StoreProductPeriodSerializer
from .utils import get_query_params

# from auth
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from djoser import views

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .serializers import (MeUserSerializer, CustomUserCreateSerializer)
from .serializers import RefreshTokenSerializer

# from select
from rest_framework import filters
from rest_framework.exceptions import ValidationError

from .filters.filters_trial_2 import (
    ShopFilter, GroupFilterForValidate, CategoryFilterForValidate
)
from .serializers import CategorySerializersCategorySerialiser
from .serializers import ProductSerializersProductSerialiser
from .serializers import (
    CategoriesWithSalesSerializer, GroupWithSalesSerializer,
    SubcategoriesWithSalesSerializer)

# from views_forecast
from .filters.filter_forecast import ForecastByShopFilter
from .serializers import ForecastForecastSerializer


# from new_sales_views
class NewSaleSerializer(serializers.ModelSerializer):
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
    serializer_class = NewSaleSerializer

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


# from view_forecast
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
class ForecastForecastViewSet(viewsets.ModelViewSet):
    serializer_class = ForecastForecastSerializer
    queryset = Forecast.objects.all()
    filter_backends = (ForecastByShopFilter,)

    def get_queryset(self):
        res = super().get_queryset()
        return res


# from select
class ProductSelectFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if ('store' not in request.query_params
                or 'group' not in request.query_params
                or 'category' not in request.query_params
                or 'subcategory' not in request.query_params):
            raise ValidationError('An ass happen')
        res = (
            queryset.filter(
                sales__st_id=(request.query_params['store']),
                pr_subcat_id__cat_id__group_id=request.query_params['group'],
                pr_subcat_id=request.query_params['subcategory'],
                pr_subcat_id__cat_id=request.query_params['category'],
                sales__pr_sales_type_id=False
            )
        )
        return res.distinct('pr_sku_id')


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=12
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=1
            ),
            OpenApiParameter(
                'category', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=9
            ),
            OpenApiParameter(
                'subcategory', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True, default=33
            ),
        ]
    )
)
class ProductSelectViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializersProductSerialiser
    queryset = Product.objects.all()
    filter_backends = (ProductSelectFilter,)


class CategorySelectFilter(filters.BaseFilterBackend):

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
class CategorySelectViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializersCategorySerialiser
    queryset = Category.objects.all()
    filter_backends = (CategorySelectFilter,)


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить группы',
        description='Возвращает группы в которых были продажи товаров.',
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY
            )
        ]
    )
)
class GroupsWithSalesInShop(viewsets.ModelViewSet):
    serializer_class = GroupWithSalesSerializer
    queryset = Shop.objects.all()
    filter_backends = (ShopFilter,)


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить категории.',
        description=('Возвращает категории в которых были продажи. '
                     'id магазина обязательный параметр'),
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            )
        ]
    )
)
class CategoriesWithSalesInShop(viewsets.ModelViewSet):
    serializer_class = CategoriesWithSalesSerializer
    queryset = Shop.objects.all()
    filter_backends = (ShopFilter, GroupFilterForValidate)


@extend_schema(tags=['Фильтры'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить подкатегории',
        description='Возвращает подкатегории, в которых были продажи',
        parameters=[
            OpenApiParameter(
                'store', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'group', OpenApiTypes.INT, OpenApiParameter.QUERY,
                required=True
            ),
            OpenApiParameter(
                'category', OpenApiTypes.INT, OpenApiParameter.QUERY
            )
        ]
    )
)
class SubcategoriesWithSalesInShop(viewsets.ModelViewSet):
    serializer_class = SubcategoriesWithSalesSerializer
    queryset = Shop.objects.all()
    filter_backends = (ShopFilter, GroupFilterForValidate,
                       CategoryFilterForValidate)


# from auth
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
    serializer_class = CustomUserCreateSerializer


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


@extend_schema(tags=['Пользователь'])
@extend_schema_view(
    post=extend_schema(
        summary='Логаут',
        description='''Удаляет refresh token. Для логаута на фронте надо
        удалить access token. '''
    )
)
class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# from base
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
            return HttpResponse('Неподдерживаемый формат файла',
                                status=HTTPStatus.BAD_REQUEST)

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
            response[
                'Content-Disposition'
            ] = f'attachment; filename="forecast.{filetype}"'

        return response


@extend_schema(tags=['Справочник'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список продаж'
    )
)
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = MaxLimitLimitOffsetPagination
    http_method_names = ('get', 'post',)

    @action(detail=False, methods=['post'],
            url_name='upload',
            url_path='upload')
    def upload(self, request):
        if len(request.FILES) != 1:
            return HttpResponse('Вложите один файл для импорта',
                                status=HTTPStatus.BAD_REQUEST)
        file = next(request.FILES.values())
        df = pd.read_csv(file)

        sales = []
        try:
            for _, row in df.iterrows():
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
            return HttpResponse('Неверный формат столбцов',
                                status=HTTPStatus.CREATED)
        Sale.objects.bulk_create(sales)

        return HttpResponse('Импорт продаж завершен',
                            status=HTTPStatus.CREATED)


@extend_schema(tags=['Справочник'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список категорий'
    )
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=['Справочник'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить группы товаров'
    )
)
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@extend_schema(tags=['Справочник'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список дивизионов'
    )
)
class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


@extend_schema(tags=['Справочник'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список ТЦ'
    )
)
class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


@extend_schema(tags=['Справочник'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список товаров'
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = MaxLimitLimitOffsetPagination


@extend_schema(tags=['Справочник'])
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
