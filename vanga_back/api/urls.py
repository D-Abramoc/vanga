from django.urls import include, path
from rest_framework import routers

from .views import ShopViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'shops', ShopViewSet, basename='shops')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

