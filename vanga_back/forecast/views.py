from rest_framework.decorators import api_view
from django.http import HttpResponse

from .functions import get_forecast


@api_view(http_method_names=['POST'])
def receive_status(request):
    """Получение информации о готовности прогноза и запуск трансфера данных"""
    if request.POST['status'] == 'ready':
        get_forecast()
    return HttpResponse(status=200)
