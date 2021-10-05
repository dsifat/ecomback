from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, serializers, status


from apps.ecommerce.models import Product, Category, DiscountCategory
from apps.ecommerce.serializers import ProductSerializer, CategorySerializer, DCSerializer


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'discount_category']

    # authentication_classes = [TokenAuthentication]
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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


