from djoser import views
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from ..serializers import MeUserSerializer


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
