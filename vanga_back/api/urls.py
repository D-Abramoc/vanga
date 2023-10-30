from django.urls import include, path
from rest_framework import routers

from .routers import OnlyGetRouter
from .views import (CityViewSet, DivisionViewSet,
                    ForecastViewSet, GetSalesViewSet, GroupViewSet,
                    SaleViewSet, ShopViewSet, CategoryViewSet,
                    ProductViewSet, NewSalesViewSet, ForecastForecastViewSet,
                    CustomTokenViewSet, CustomUserViewSet, LogoutView,
                    MeUserViewSet, RefreshTokenViewSet,
                    CategoriesWithSalesInShop,
                    CategorySelectViewSet,
                    GroupsWithSalesInShop, ProductSelectViewSet,
                    SubcategoriesWithSalesInShop)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1_only_get = OnlyGetRouter()

router_v1.register(r'forecasts', ForecastViewSet, basename='forecasts')
router_v1_only_get.register(r'shops', ShopViewSet, basename='shops')
router_v1_only_get.register(
    r'products', ProductViewSet, basename='products'
)
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
    path(
        'v1/forecast/get_forecast/',
        ForecastForecastViewSet.as_view({'get': 'list'})
    ),
    path(
        'v1/sales/store_product_period',
        GetSalesViewSet.as_view({'get': 'list'})
    ),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/users/', CustomUserViewSet.as_view({'post': 'create'})),
    path('auth/jwt/create/', CustomTokenViewSet.as_view()),
    path('auth/jwt/refresh/', RefreshTokenViewSet.as_view()),
    path('auth/users/me/', MeUserViewSet.as_view({'get': 'me'})),
    path(
        'v1/filters/products/', ProductSelectViewSet.as_view({'get': 'list'})
    ),
    path(
        'v1/filters/category/', CategorySelectViewSet.as_view({'get': 'list'})
    ),
    path(
        'v1/filters/groups_whith_sales/',
        GroupsWithSalesInShop.as_view({'get': 'list'})
    ),
    path('v1/filters/categories_with_sales/',
         CategoriesWithSalesInShop.as_view({'get': 'list'})),
    path('v1/filters/subcategories_with_sales/',
         SubcategoriesWithSalesInShop.as_view({'get': 'list'})),
    path('v1/', include(router_v1_only_get.urls)),
    path('v1/', include(router_v1.urls)),
]
