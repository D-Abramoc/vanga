from django.urls import include, path
from rest_framework import routers

from .views import (CityViewSet, ProductViewSet, ShopViewSet, ForecastViewSet,
                    SaleViewSet, CategoryViewSet, GroupViewSet,
                    DivisionViewSet)
from .custom_routers import OnlyGetRouter


app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1_only_get = OnlyGetRouter()

router_v1.register(r'forecasts', ForecastViewSet, basename='forecasts')
router_v1.register('sales', SaleViewSet, basename='sales')
router_v1_only_get.register(r'shops', ShopViewSet, basename='shops')
router_v1_only_get.register(r'products', ProductViewSet, basename='products')
router_v1_only_get.register(r'cities', CityViewSet, basename='cities')
router_v1_only_get.register(r'categories', CategoryViewSet, basename='categories')
router_v1_only_get.register(r'groups', GroupViewSet, basename='groups')
router_v1_only_get.register(r'divisions', DivisionViewSet, basename='divisions')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1_only_get.urls)),
    path('v1/', include(router_v1.urls))
]

