from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet, ShopViewSet
from .custom_routers import OnlyGetRouter


app_name = 'api'

router_v1 = OnlyGetRouter()

router_v1.register(r'shops', ShopViewSet, basename='shops')
router_v1.register(r'categories', ProductViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

