from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.ecommerce.models import Product
from apps.ecommerce.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = []
    queryset = Product.objects.all()
