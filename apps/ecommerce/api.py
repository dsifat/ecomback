from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.ecommerce.models import Product, Category, DiscountCategory
from apps.ecommerce.serializers import ProductSerializer, CategorySerializer, DCSerializer


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'discount_category']

    # authentication_classes = [TokenAuthentication]
    queryset = Product.objects.all()

    @action(methods=['get'],detail=False, permission_classes=[],
            url_path='hello', url_name='hello')
    def hello(self, request, *args, **kwargs):
        query = Product.objects.all()
        return Response(data={"msg":"hello world"}, status=200)

    def list(self, request, *args, **kwargs):
        return Response(data={"msg":"hello world"}, status=200)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = []
    permission_classes = []
    queryset = Category.objects.all()


class DCViewset(viewsets.ModelViewSet):
    serializer_class = DCSerializer
    authentication_classes = []
    permission_classes = []
    queryset = DiscountCategory.objects.all()