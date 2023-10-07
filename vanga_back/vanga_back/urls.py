from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
        name='docs'
    ),
    path(
        'api/redoc/', SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
    path('api/', include('api.urls', namespace='api')),
    path('api/', include('forecast.urls', namespace='forecast'))
]
