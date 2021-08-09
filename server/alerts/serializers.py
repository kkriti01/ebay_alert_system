from rest_framework import serializers
from .models import ProductAlert


class ProductAlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAlert
        fields = '__all__'
