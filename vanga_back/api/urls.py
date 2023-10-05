from django.urls import include, path
from rest_framework import routers

from .routers import OnlyGetRouter
from .views import (CustomUserViewSet, CategoryViewSet, CityViewSet,
                    DivisionViewSet, ForecastViewSet, GroupViewSet,
                    ProductViewSet, ShopViewSet, SaleViewSet,
                    CustomTokenViewSet, MeUserViewSet,
                    GetSalesViewSet, RefreshTokenViewSet)
from .views_logout import LogoutView

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1_only_get = OnlyGetRouter()

router_v1.register(r'forecasts', ForecastViewSet, basename='forecasts')
router_v1_only_get.register('sales', SaleViewSet, basename='sales')
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
    path('auth/logout/', LogoutView.as_view()),
    path('auth/users/', CustomUserViewSet.as_view({'post': 'create'})),
    path('auth/jwt/create/', CustomTokenViewSet.as_view()),
    path('auth/jwt/refresh/', RefreshTokenViewSet.as_view()),
    path('auth/users/me/', MeUserViewSet.as_view({'get': 'me'})),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    path(
        'v1/sales/store_product_period',
        GetSalesViewSet.as_view({'get': 'list'})
    ),
    path('v1/', include(router_v1_only_get.urls)),
    path('v1/', include(router_v1.urls)),
]
