from rest_framework import serializers

from backend.models import City, Shop


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


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
