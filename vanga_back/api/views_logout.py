from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers_logout import RefreshTokenSerializer


@extend_schema(tags=['Пользователь'])
@extend_schema_view(
    post=extend_schema(
        summary='Логаут',
        description='''Для логаута на фронтенде надо скинуть access token.
        Эта ручка удалит переданный refresh token и в дальнейшем по этому
        токену нельзя будет обновить accsess.'''
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
