from djoser import views
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from ..serializers.serializers import MeUserSerializer
from ..serializers.serializers_logout import RefreshTokenSerializer


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
