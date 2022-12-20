import requests
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from decouple import config
from apps.ecommerce.models import Product, Category, DiscountCategory, MainBanner, Order
from apps.ecommerce.serializers import ProductSerializer, CategorySerializer, DCSerializer, MainBannerSerializer, \
    OrderSerializer


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'featured', 'new']

    # authentication_classes = [TokenAuthentication]
    queryset = Product.objects.all()


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

class MainBannerApi(viewsets.ModelViewSet):
    serializer_class = MainBannerSerializer
    authentication_classes = []
    permission_classes = []
    queryset = MainBanner.objects.all()
    http_method_names = ['get']

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = []
    permission_classes = []
    queryset = Order.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch','delete']

SSLCZ_SESSION_API = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'

def sslcommerze_get(price, order):
    post_data = {}
    price = price
    order = order
    post_data['store_id'] = "redsw63984ec315c0a"
    post_data['store_passwd'] = "redsw63984ec315c0a@ssl"
    post_data['total_amount'] = 50
    post_data['currency'] = "BDT"
    post_data['tran_id'] = "1212"
    protocol = "http"
    # if request.is_secure():
    #     protocol = "https"
    # else:
    protocol = "http"
    post_data['success_url'] = "http://127.0.0.1:9000/api/v1/payment/sslcommerz/success/"
    post_data['fail_url'] = "http://127.0.0.1:9000/sslcommerze/fail/"
    post_data['cancel_url'] = "http://127.0.0.1:9000/sslcommerze/cancel/"

    # CUSTOMER INFORMATION
    post_data['cus_name'] = "sdasd"
    post_data['cus_email'] = "a@a.com"
    post_data['cus_add1'] = "N/A"
    post_data['cus_city'] = "Rajshahi"
    post_data['cus_country'] = "Bangladesh"
    post_data['cus_phone'] = "01833184071"

    # SHIPMENT INFORMATION
    post_data['shipping_method'] = "NO"

    post_data["product_name"] = "Pet Animal License"
    post_data["product_category"] = "License"
    post_data["product_profile"] = "General"

    response = requests.post(SSLCZ_SESSION_API, post_data)
    return (response.json()["sessionkey"],response.json()["GatewayPageURL"])

class SSLGetSessionView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        price = request.query_params.get('price')
        order = request.query_params.get('order')
        session, gateway = sslcommerze_get(price, order)
        return Response(data={"session":session,"gateway":gateway},status=status.HTTP_200_OK)

class SSLCommerzSuccess(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    def post(self, request, format=None):
        FRONTEND_SUCCESS_URL = config('FRONTEND_SUCCESS_URL', default="http://localhost:3000/payment/success/")
        transaction = request.POST.get("tran_id")
        return HttpResponseRedirect(FRONTEND_SUCCESS_URL)