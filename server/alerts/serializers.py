from rest_framework import serializers
from .models import ProductAlert, Product


class ProductAlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAlert
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
