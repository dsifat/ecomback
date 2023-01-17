from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.ecommerce.models import Order
from apps.ecommerce.serializers import OrderSerializer


class OrderCount(ListAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'created_at':['date__range'],
    }