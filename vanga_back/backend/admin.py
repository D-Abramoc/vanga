from django.contrib import admin

from .models import (City, Division, Shop, Group, Category, Subcategory,
                     Product, Sale)


admin.site.register((City, Division, Shop, Group, Category, Subcategory,
                     Product, Sale))
