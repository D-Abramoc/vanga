from rest_framework import serializers

from backend.models import (Shop, Group, Product, Subcategory, Category,
                            Sale)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


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
        fields = '__all__'

    def get_categories(self, obj):
        '''Возвращает категории по которым в магазине были продажи'''
        sales = Sale.objects.filter(st_id=self.context['shop'], pr_sales_type_id=False)
        products = Product.objects.filter(sales__in=sales)
        subcategories = Subcategory.objects.filter(products__in=products)
        queryset = (
            Category.objects
            .filter(subcategories__in=subcategories)
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
        '''Возвращает группы по которым в магазине были продажи'''
        sales = Sale.objects.filter(st_id=obj, pr_sales_type_id=False)
        products = Product.objects.filter(sales__in=sales)
        subcategories = Subcategory.objects.filter(products__in=products)
        categories = Category.objects.filter(subcategories__in=subcategories)
        queryset = (
            Group.objects.filter(categories__in=categories)
            .distinct().order_by('id')
        )
        if 'group' in self.context['request'].query_params:
            queryset = queryset.filter(id=int(self.context['request'].query_params['group']))
        serialiser = GroupCategorySerializer(
            queryset, many=True, context={
                'shop': obj
            }
        )
        return serialiser.data


class SubcategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class SubcategoriesWithSalesSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField('get_categories')

    class Meta:
        model = Category
        fields = ('categories',)

    def get_categories(self, obj):
        '''Возвращает группы по которым в магазине были продажи'''
        sales = Sale.objects.filter(st_id=obj, pr_sales_type_id=False)
        products = Product.objects.filter(sales__in=sales)
        subcategories = Subcategory.objects.filter(products__in=products)
        queryset = (
            Category.objects
            .filter(subcategories__in=subcategories)
            .distinct()
        )
        if 'group' in self.context['request'].query_params:
            queryset = queryset.filter(
                id=int(self.context['request'].query_params['group'])
            )
        serializer = CategorySubSerializer(queryset, many=True)
        return serializer.data
