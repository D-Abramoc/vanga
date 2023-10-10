import json
from datetime import datetime

import requests

from backend.models import Product, Sale, Shop

from .models import Forecast


def get_forecast(ds_url: str) -> list[dict]:
    """Получение прогнозных данных с сервера ML"""
    url: str = f'{ds_url}/get_predict'
    response = requests.get(url).json()
    json_response = json.loads(response)
    return json_response


def save_forecast(fc_json: list[dict]) -> None:
    """Сохранение полученного от ML прогноза в базу"""
    calc_date = datetime.now().date()
    forecasts: list = []
    for forecast in fc_json:
        forecasts.append(Forecast(
            calc_date=calc_date,
            st_id=Shop.objects.get(st_id=forecast['st_id']),
            pr_sku_id=Product.objects.get(pr_sku_id=forecast['pr_sku_id']),
            date=forecast['date'],
            target=forecast['target']))
    Forecast.objects.bulk_create(forecasts)


def send_sales_to_ds(array: list[type[Sale]], ds_url: str) -> None:
    """Отправка новых данных о продажах на сервер ML"""
    url: str = f'{ds_url}/update_sales'
    sales_to_send = []
    for sale in array:
        sales_to_send.append(sale.to_dict())
    requests.post(url, json=json.dumps(sales_to_send))
