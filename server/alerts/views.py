from rest_framework import viewsets

from .models import ProductAlert, Product
from .serializers import ProductAlertSerializer


class UserProductAlertViewSet(viewsets.ModelViewSet):
    """
    Simple model viewSet to create, update and delete product alert
    """
    serializer_class = ProductAlertSerializer
    http_method_names = ['get', 'put', 'post', 'patch', 'delete']
    queryset = ProductAlert.objects.all()


class UserProductViewSet(viewsets.ModelViewSet):
    """
    Simple model viewSet to create, update and delete product alert
    """
    serializer_class = ProductSerializer
    http_method_names = ['get', 'put', 'post', 'patch', 'delete']
    queryset = Product.objects.all()
