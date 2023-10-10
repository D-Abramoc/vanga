from rest_framework import serializers

from backend.models import Category, Group, Product, Sale, Shop, Subcategory
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


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


class SubcategoriesSerializer(serializers.ModelSerializer):
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
        serializer = SubcategoriesSerializer(
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
