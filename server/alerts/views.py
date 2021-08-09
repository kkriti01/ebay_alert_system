from rest_framework import viewsets

from .models import ProductAlert
from .serializers import ProductAlertSerializer


class UserProductAlertViewSet(viewsets.ModelViewSet):
    """
    Simple model viewSet to create, update and delete product alert
    """
    serializer_class = ProductAlertSerializer
    http_method_names = ['get', 'put', 'post', 'patch', 'delete']
    queryset = ProductAlert.objects.all()
