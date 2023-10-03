from rest_framework import serializers

from backend.models import Shop, Product, Sale


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
            obj.products.filter(st_id__in=self.context['query']['store'])
            .filter(date__range=[self.context['query']['start_date'][0],
                                 self.context['query']['end_date'][0]])
        )
        serializer = SaleSerializer(queryset, many=True)
        return serializer.data


class TSerializer(serializers.ModelSerializer):
    goods = serializers.SerializerMethodField('get_goods')

    class Meta:
        model = Shop
        fields = ('id', 'st_id', 'goods',)

    def get_goods(self, obj):
        products_unique = (
            obj.stores.filter(date__range=[
                self.context['query']['start_date'][0],
                self.context['query']['end_date'][0]
            ])
            .filter(pr_sku_id__in=self.context['query']['sku'])
            .values('pr_sku_id').distinct()
        )
        products_id = [i['pr_sku_id'] for i in products_unique]
        queryset = Product.objects.filter(id__in=products_id).order_by('id')
        serializer = GoodsSerializer(queryset, many=True,
                                     context={'query': self.context['query']})
        return serializer.data
