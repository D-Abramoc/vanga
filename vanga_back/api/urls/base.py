from django.urls import include, path
from rest_framework import routers

from ..routers import OnlyGetRouter
from ..views_old import (CategoryViewSet, CityViewSet,
                         DivisionViewSet, ForecastViewSet, GroupViewSet,
                         ProductViewSet, ShopViewSet,
                         GetSalesViewSet,
                         SaleViewSet)
from ..views_forecast import ForecastViewSet as ForecastVS
from ..new_sales_views import NewSalesViewSet
from .auth import urlpatterns as auth_urls
from .selects import urlpatterns as filtres_urls

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1_only_get = OnlyGetRouter()

router_v1.register(r'forecasts', ForecastViewSet, basename='forecasts')
router_v1_only_get.register(r'shops', ShopViewSet, basename='shops')
router_v1_only_get.register(r'products', ProductViewSet, basename='products')
router_v1_only_get.register(r'cities', CityViewSet, basename='cities')
router_v1_only_get.register(
    r'categories', CategoryViewSet, basename='categories'
)
router_v1_only_get.register(r'groups', GroupViewSet, basename='groups')
router_v1_only_get.register(
    r'divisions', DivisionViewSet, basename='divisions'
)
router_v1.register(r'sales', SaleViewSet, basename='sales')

urlpatterns = [
    path('v1/get_sales/', NewSalesViewSet.as_view({'get': 'list'})),
    path('v1/filters/', include(filtres_urls)),
    path('v1/forecast/get_forecast/', ForecastVS.as_view({'get': 'list'})),
    path('auth/', include(auth_urls)),
    path(
        'v1/sales/store_product_period',
        GetSalesViewSet.as_view({'get': 'list'})
    ),
    path('v1/', include(router_v1_only_get.urls)),
    path('v1/', include(router_v1.urls)),
]
