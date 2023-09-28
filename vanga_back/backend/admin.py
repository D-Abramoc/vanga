from django.contrib import admin

from .models import (Category, City, Division, Group, Product, Sale, Shop,
                     Subcategory)

admin.site.register((City, Division, Shop, Group, Category, Subcategory,
                     Product, Sale))
