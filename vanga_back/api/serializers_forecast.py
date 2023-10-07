from rest_framework import serializers

from backend.models import Shop, Product
from forecast.models import Forecast


class PredictSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forecast
        fields = ('date', 'target')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        return res


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

    def to_representation(self, instance):
        res = super().to_representation(instance)
        return res


class ForecastSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        res = super().to_representation(instance)
        return res
