from django.contrib import admin

from .models import Forecast


class ForecastAdmin(admin.ModelAdmin):
    list_display = ('id', 'st_id', 'pr_sku_id', 'date', 'target')
    list_filter = ('st_id', 'pr_sku_id', 'date',)


admin.site.register(Forecast, ForecastAdmin)
