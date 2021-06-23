from rest_framework import viewsets

from apps.ecommerce.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []
