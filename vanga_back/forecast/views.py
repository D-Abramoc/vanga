from http.client import BAD_REQUEST, CREATED

from django.http import HttpResponse
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)

from forecast.config import DS_URL

from .functions import get_forecast, save_forecast


@api_view(http_method_names=['POST'])
@authentication_classes([])
@permission_classes([])
def receive_status(request):
    """Получение информации о готовности прогноза и запуск трансфера данных"""
    try:
        if request.POST['status'] == 'ready':
            fc_json = get_forecast(DS_URL)
            save_forecast(fc_json)
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
