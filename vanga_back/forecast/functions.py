import requests
import json
from datetime import datetime

from .models import Forecast
from backend.models import Shop, Product


def get_forecast():
    """Получение прогнозных данных с сервера ML и сохранение в базу"""
    url = 'http://127.0.0.1:8000/get_predict'
    response = requests.get(url).json()
    json_response = json.loads(response)
    calc_date = datetime.now().date()
    forecasts = []
    for forecast in json_response:
        forecasts.append(Forecast(
            calc_date=calc_date,
            st_id=Shop.objects.get(st_id=forecast['st_id']),
            pr_sku_id=Product.objects.get(pr_sku_id=forecast['pr_sku_id']),
            date=forecast['date'],
            target=forecast['target']))
    Forecast.objects.bulk_create(forecasts)
    print('Импорт прогнозов завершён.')
