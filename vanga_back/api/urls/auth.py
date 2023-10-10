from django.urls import path

from ..views_logout import LogoutView
from ..views.auth import (MeUserViewSet, CustomUserViewSet,
                          CustomTokenViewSet, RefreshTokenViewSet)


urlpatterns = [
    path('logout/', LogoutView.as_view()),
    path('users/', CustomUserViewSet.as_view({'post': 'create'})),
    path('jwt/create/', CustomTokenViewSet.as_view()),
    path('jwt/refresh/', RefreshTokenViewSet.as_view()),
    path('users/me/', MeUserViewSet.as_view({'get': 'me'})),
]
