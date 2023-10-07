from rest_framework import serializers

from backend.models import Category


class CategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
