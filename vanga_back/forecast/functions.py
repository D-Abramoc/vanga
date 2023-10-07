import requests
import json
from datetime import datetime

from .config import DS_URL
from .models import Forecast
from backend.models import Shop, Product, Sale


def get_forecast() -> None:
    """Получение прогнозных данных с сервера ML и сохранение в базу"""
    url: str = f'{DS_URL}/get_predict'
    response = requests.get(url).json()
    json_response = json.loads(response)
    calc_date = datetime.now().date()
    forecasts: list = []
    for forecast in json_response:
        forecasts.append(Forecast(
            calc_date=calc_date,
            st_id=Shop.objects.get(st_id=forecast['st_id']),
            pr_sku_id=Product.objects.get(pr_sku_id=forecast['pr_sku_id']),
            date=forecast['date'],
            target=forecast['target']))
    Forecast.objects.bulk_create(forecasts)


def send_sales_to_ds(array: list[type[Sale]]) -> None:
    """Отправка новых данных о продажах на сервер ML"""
    url: str = f'{DS_URL}/update_sales'
    sales_to_send = []
    for sale in array:
        sales_to_send.append(sale.to_dict())
    requests.post(url, json=json.dumps(sales_to_send))
