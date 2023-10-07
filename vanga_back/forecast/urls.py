from django.urls import path

from .views import receive_status

app_name = 'forecast'

urlpatterns = [
    path('v1/ready', receive_status),
]
