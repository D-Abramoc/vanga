from rest_framework.pagination import LimitOffsetPagination


class MaxLimitLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100
