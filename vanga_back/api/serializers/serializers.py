from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer

from backend.models import (Category, City, Division, Group, Product, Sale,
                            Shop, Subcategory)
from forecast.models import Forecast
from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class MeUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['email']


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)

    def validate(self, attrs):
        if 'email' not in attrs:
            raise ValidationError('This field is required.')
        if User.objects.filter(email=attrs['email']).exists():
            raise ValidationError(
                'Пользователь с такой почтой уже зарегистрирован.'
            )
        return super().validate(attrs)

    def perform_create(self, validated_data):
        if 'username'not in validated_data:
            try:
                validated_data['username'] = validated_data['email']
            except KeyError:
                raise ValidationError('Email required.')
        return super().perform_create(validated_data)


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    store = serializers.CharField(source='st_id')
    city = serializers.CharField(source='st_city_id.city_id')
    division = serializers.CharField(
        source='st_division_code_id.division_code_id'
    )
    type_format = serializers.IntegerField(source='st_type_format_id')
    loc = serializers.IntegerField(source='st_type_loc_id')
    size = serializers.IntegerField(source='st_type_size_id')
    is_active = serializers.BooleanField(source='st_is_active')

    class Meta:
        model = Shop
        exclude = ['st_id', 'st_city_id', 'st_division_code_id',
                   'st_type_format_id', 'st_type_loc_id', 'st_type_size_id',
                   'st_is_active']


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source='pr_sku_id')
    # group = serializers.CharField(
    #     source='pr_subcat_id.cat_id.group_id.group_id'
    # )
    # category = serializers.CharField(source='pr_subcat_id.cat_id.cat_id')
    # subcategory = serializers.CharField(source='pr_subcat_id.subcat_id')
    # uom = serializers.IntegerField(source='pr_uom_id')

    class Meta:
        model = Product
        fields = ('id', 'sku')
        # exclude = ['pr_uom_id', 'pr_subcat_id', 'pr_sku_id']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DefaultShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ('st_id', 'pr_sku_id', 'date', 'pr_sales_in_units',)

    def to_representation(self, instance):
        return super().to_representation(instance)


class TestProductSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_sales')

    class Meta:
        model = Product
        fields = ('id', 'pr_sku_id', 'data',)

    def get_sales(self, obj):
        page_size = 100
        paginator = Paginator(obj.products.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1
        sales = paginator.page(page)
        serializer = TestSaleSerializer(
            sales, many=True, context={'request': self.context['request']}
        )
        return serializer.data


class TestSubcategorySerializer(serializers.ModelSerializer):
    subcategories = TestProductSerializer(many=True)

    class Meta:
        model = Subcategory
        fields = ('id', 'subcat_id', 'subcategories')


class TestCategorySerializer(serializers.ModelSerializer):
    categories = TestSubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'cat_id', 'categories',)


class TestGroupSerializer(serializers.ModelSerializer):
    groups = TestCategorySerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'group_id', 'groups')


class TestSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
