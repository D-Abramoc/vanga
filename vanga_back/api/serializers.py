from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer

from backend.models import (Category, City, Division, Group, Product, Sale,
                            Shop, Subcategory)
from forecast.models import Forecast
from users.models import User
from django.db.models import QuerySet
from .utils import get_query_params
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = ('date', 'target')


class ProductsForecastSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='pr_sku_id.id', read_only=True
    )
    pr_sku_id = serializers.SlugRelatedField(
        slug_field='pr_sku_id',
        queryset=Product.objects.all()
    )
    pr_uom_id = serializers.SerializerMethodField('get_pr_uom_id')
    predict = serializers.SerializerMethodField('get_predict')

    class Meta:
        model = Forecast
        fields = ('id', 'pr_sku_id', 'pr_uom_id', 'predict')

    def get_pr_uom_id(self, obj):
        return obj.pr_sku_id.pr_uom_id

    def get_predict(self, obj):
        queryset = Forecast.objects.filter(pr_sku_id=obj.pr_sku_id,
                                           st_id=obj.st_id)
        serializer = PredictSerializer(queryset, many=True)
        return serializer.data


class ForecastForecastSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='st_id.id',
                                            read_only=True)
    st_id = serializers.SlugRelatedField(
        slug_field='st_id',
        queryset=Shop.objects.all()
    )
    product = serializers.SerializerMethodField('get_product')

    class Meta:
        model = Forecast
        fields = ('id', 'st_id', 'product')

    def get_product(self, obj):
        serializer = ProductsForecastSerializer(obj)
        return serializer.data


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ProductSerializersProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'pr_sku_id')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid Example',
            value={
                "id": 12,
                "st_id": "084a8a9aa8cced9175bd07bc44998e75",
                "groups": [
                    {
                        "id": 1,
                        "group_id": "c74d97b01eae257e44aa9d5bade97baf"
                    },
                ]
            }
        )
    ]
)
class GroupWithSalesSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField('get_groups')

    class Meta:
        model = Shop
        fields = ('id', 'st_id', 'groups')

    def get_groups(self, obj):
        '''Возвращает группы по которым в магазине были продажи'''
        sales = Sale.objects.filter(st_id=obj, pr_sales_type_id=False)
        products = Product.objects.filter(sales__in=sales)
        subcategories = Subcategory.objects.filter(products__in=products)
        categories = Category.objects.filter(subcategories__in=subcategories)
        queryset = (
            Group.objects.filter(categories__in=categories)
            .distinct().order_by('id')
        )
        serialiser = GroupSerializer(queryset, many=True)
        return serialiser.data


class GroupCategorySerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField('get_categories')

    class Meta:
        model = Group
        fields = ('id', 'categories',)

    def get_categories(self, obj):
        """Возвращает категории по которым в магазине были продажи."""
        queryset = (
            Category.objects
            .filter(subcategories__products__sales__pr_sales_type_id=False,
                    subcategories__products__sales__st_id=self.context['shop'],
                    group_id=self.context['group'])
            .distinct()
            .order_by('id')
        )
        serialiser = CategorySerializer(queryset, many=True)
        return serialiser.data


class CategoriesWithSalesSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField('get_groups')

    class Meta:
        model = Shop
        fields = ('groups',)

    def get_groups(self, obj):
        """Возвращает группы по которым в магазине были продажи."""
        queryset = (
            Group.objects
            .filter(
                categories__subcategories__products__sales__pr_sales_type_id=False,  # noqa
                categories__subcategories__products__sales__st_id=obj
            ).distinct().order_by('id')
        )
        if 'group' in self.context['request'].query_params:
            queryset = queryset.filter(
                id=int(self.context['request'].query_params['group'])
            )
        serialiser = GroupCategorySerializer(
            queryset, many=True, context={
                'shop': obj,
                'group': self.context['request'].query_params['group']
            }
        )
        return serialiser.data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        return res


class FilterSubcategoriesSerialiser(serializers.ListSerializer):

    def to_representation(self, data):
        if 'category' not in self.context['params']:
            return super().to_representation(data)
        return super().to_representation(
            data.filter(id=self.context['params']['category'])
        )


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySubSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField('get_subcats')

    class Meta:
        model = Category
        fields = ('id', 'cat_id', 'group_id', 'subcategories')

    def get_subcats(self, obj):
        queryset = (
            Subcategory.objects.filter(
                products__sales__pr_sales_type_id=False,
                cat_id=self.context['params']['category'],
                cat_id__group_id=self.context['params']['group'],
                products__sales__st_id=self.context['params']['store']
            ).distinct('subcat_id')
        )
        serializer = SubcategorySerializer(
            queryset, many=True, context={'params': self.context['params']}
        )
        return serializer.data


class SubcategoriesWithSalesSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField('get_categories')

    class Meta:
        model = Category
        fields = ('categories',)

    def get_categories(self, obj):
        '''Возвращает группы по которым в магазине были продажи'''
        queryset = (
            Category.objects
            .filter(
                subcategories__products__sales__pr_sales_type_id=False,
                subcategories__products__sales__st_id=(self.context['request']
                                                       .query_params['store']),
                group_id=self.context['request'].query_params['group']
            ).distinct()
        )
        if 'group' in self.context['request'].query_params:
            queryset = queryset.filter(
                group_id=int(self.context['request'].query_params['group'])
            )
        serializer = CategorySubSerializer(
            queryset, many=True,
            context={'params': self.context['request'].query_params}
        )
        return serializer.data


# from serializers_trial
class ProdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pr_uom_id',)


class SaleSerializersTrialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ('date', 'pr_sales_in_units',)


class GoodsSerializer(serializers.ModelSerializer):
    sales = serializers.SerializerMethodField('get_sales')

    class Meta:
        model = Product
        fields = ('id', 'pr_sku_id', 'pr_uom_id', 'sales',)

    def get_sales(self, obj):
        queryset = (
            obj.sales.filter(st_id__in=self.context['params']['store'])
            .filter(date__range=[self.context['params']['start_date'][0],
                                 self.context['params']['end_date']])
            .filter(pr_sales_type_id=True)
        )
        serializer = SaleSerializersTrialSerializer(queryset, many=True)
        return serializer.data


class StoreProductPeriodSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_products')

    class Meta:
        model = Shop
        fields = ('id', 'st_id', 'products',)

    def get_products(self, obj: Shop):
        params: dict[str, list[str] | str] = get_query_params(
            self.context.get('request').query_params
        )
        if ('start_date' not in params
                or 'end_date' not in params
                or 'sku' not in params):
            raise serializers.ValidationError(
                'Отсутствует одно или несколько обязательных полей'
            )
        products_unique: QuerySet = (
            obj.sales.filter(date__range=[
                params['start_date'][0],
                params['end_date']
            ])
            .filter(pr_sku_id__in=params['sku'], pr_sales_type_id=False)
            .values('pr_sku_id').distinct()
        )
        products_id = [i['pr_sku_id'] for i in products_unique]
        queryset = Product.objects.filter(id__in=products_id).order_by('id')
        serializer = GoodsSerializer(queryset, many=True,
                                     context={'params': params})
        return serializer.data


# serializers
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


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source='pr_sku_id')

    class Meta:
        model = Product
        fields = ('id', 'sku')


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


class NewSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('date', 'pr_sales_in_units')
