from django.urls import include, path
from rest_framework import routers

from .custom_routers import OnlyGetRouter
from .views import (CustomUserViewSet, CategoryViewSet, CityViewSet,
                    DivisionViewSet, ForecastViewSet, GroupViewSet,
                    ProductViewSet, SaleViewSet, ShopViewSet,
                    CustomTokenViewSet, MeUserViewSet,
                    GetProductSalesForPeriod, TestView, get_sales)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1_only_get = OnlyGetRouter()

router_v1.register(r'forecasts', ForecastViewSet, basename='forecasts')
router_v1.register('sales', SaleViewSet, basename='sales')
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

urlpatterns = [
    path('auth/users/', CustomUserViewSet.as_view({'post': 'create'})),
    path('auth/jwt/create/', CustomTokenViewSet.as_view()),
    path('auth/users/me/', MeUserViewSet.as_view({'get': 'me'})),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    path('v1/sales/test', get_sales,),
    path(
        'v1/sales/period/', GetProductSalesForPeriod.as_view({'get': 'list'})
    ),
    path('v1/', include(router_v1_only_get.urls)),
    path('v1/', include(router_v1.urls)),
]
