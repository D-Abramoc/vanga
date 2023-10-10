from rest_framework import serializers

from backend.models import Product


class ProductSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'pr_sku_id')
