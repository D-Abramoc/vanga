from http.client import BAD_REQUEST, CREATED

from django.http import HttpResponse
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)

from .functions import get_forecast


@api_view(http_method_names=['POST'])
@authentication_classes([])
@permission_classes([])
def receive_status(request):
    """Получение информации о готовности прогноза и запуск трансфера данных"""
    try:
        if request.POST['status'] == 'ready':
            get_forecast()
            return HttpResponse(status=CREATED)
        return HttpResponse(
            'Неверная информация о готовности прогноза',
            status=BAD_REQUEST
        )
    except KeyError:
        return HttpResponse(
            'Не получена информация о готовности прогноза',
            status=BAD_REQUEST
        )
