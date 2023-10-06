from django.db.models import QuerySet
from rest_framework import serializers

from backend.models import Shop, Product, Sale

from .utils import get_query_params


class ProdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pr_uom_id',)


class SaleSerializer(serializers.ModelSerializer):

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
        serializer = SaleSerializer(queryset, many=True)
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
