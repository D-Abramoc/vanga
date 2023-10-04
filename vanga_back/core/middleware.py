import time
from typing import Any

from django.utils.deprecation import MiddlewareMixin


class RequestTimeMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:
        timestmp = time.monotonic()
        response = self.get_response(request)
        print(f'Продолжительность запроса {request.path} -> '
              f'{time.monotonic() - timestmp:.3f} сек.')
        return response
