from rest_framework import serializers

from backend.models import Product, Shop, Subcategory


class ShopSerializer(serializers.ModelSerializer):
    store = serializers.CharField(source='st_id')
    city = serializers.CharField(source='st_city_id.city_id')
    division = serializers.CharField(source='st_division_code_id.division_code_id')
    type_format = serializers.IntegerField(source='st_type_format_id')
    loc = serializers.IntegerField(source='st_type_loc_id')
    size = serializers.IntegerField(source='st_type_size_id')
    is_active = serializers.BooleanField(source='st_is_active')

    class Meta:
        model = Shop
        exclude = ['id', 'st_id', 'st_city_id', 'st_division_code_id',
                   'st_type_format_id', 'st_type_loc_id', 'st_type_size_id',
                   'st_is_active']


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source='pr_sku_id')
    group = serializers.CharField(source='pr_subcat_id.cat_id.group_id.group_id')
    category = serializers.CharField(source='pr_subcat_id.cat_id.cat_id')
    subcategory = serializers.CharField(source='pr_subcat_id.subcat_id')
    uom = serializers.BooleanField(source='pr_uom_id')

    class Meta:
        model = Product
        exclude = ['id', 'pr_uom_id', 'pr_subcat_id', 'pr_sku_id']
