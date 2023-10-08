from django.contrib import admin

from .models import (Category, City, Division, Group, Product, Sale, Shop,
                     Subcategory)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_id')


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'division_code_id')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'st_id', 'st_city_id', 'st_division_code_id',
                    'st_type_format_id', 'st_type_loc_id', 'st_type_size_id',
                    'st_is_active')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_id')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_id', 'cat_id')


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_id', 'subcat_id')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'pr_sku_id', 'pr_subcat_id', 'pr_uom_id')
    list_filter = ('pr_subcat_id', 'pr_uom_id')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'st_id', 'pr_sku_id', 'date', 'pr_sales_type_id',
                    'pr_sales_in_units', 'pr_promo_sales_in_units',
                    'pr_sales_in_rub', 'pr_promo_sales_in_rub')
    list_filter = ('st_id', 'pr_sku_id', 'date')


admin.site.register(City, CityAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
