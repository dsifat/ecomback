import requests
from allauth.account.utils import send_email_confirmation
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core.management import ManagementUtility
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, serializers, status, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from decouple import config
from apps.ecommerce.models import Product, Category, DiscountCategory, MainBanner, Order, Advertisement, Subscriber, \
    User, OrderItem
from apps.ecommerce.serializers import ProductSerializer, CategorySerializer, DCSerializer, MainBannerSerializer, \
    OrderSerializer, AdvertisementSerializer, SubscriberSerializer, PasswordResetSerializer, SetNewPasswordSerializer


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['category', 'featured', 'new', 'top', 'sale']

    # authentication_classes = [TokenAuthentication]
    queryset = Product.objects.all()

    # def paginate_queryset(self, queryset):
    #     if 'page' not in self.request.query_params:
    #         return None
    #
    #     return super().paginate_queryset(queryset, request, view)

class CategoryPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = []
    permission_classes = []
    queryset = Category.objects.all()
    pagination_class = CategoryPagination


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


class AdvertisementApi(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    authentication_classes = []
    permission_classes = []
    queryset = Advertisement.objects.all()
    http_method_names = ['get']


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        items = OrderItem.objects.filter(order=order)
        context = {
            'order': order,
            'items': items,
            'user': order.user
        }
        html_email = render_to_string(template_name="email/order_create.html", context=context)
        send_mail(subject="Order Confirmation", message=html_email, html_message=html_email, fail_silently=True, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[order.user.email])

    @action(detail=False)
    def me(self, request):
        user = self.request.user
        queryset = Order.objects.filter(user=user).order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


SSLCZ_SESSION_API = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'


def sslcommerze_get(price, order):
    post_data = {}
    price = price
    order = order
    post_data['store_id'] = "redsw63984ec315c0a"
    post_data['store_passwd'] = "redsw63984ec315c0a@ssl"
    post_data['total_amount'] = price
    post_data['currency'] = "BDT"
    post_data['tran_id'] = order
    protocol = "http"
    # if request.is_secure():
    #     protocol = "https"
    # else:
    protocol = "http"
    post_data['success_url'] = "https://api.red-swiss.com/api/v1/payment/sslcommerz/success/"
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
    return (response.json()["sessionkey"], response.json()["GatewayPageURL"])


class SSLGetSessionView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        price = request.query_params.get('price')
        order = request.query_params.get('order')
        session, gateway = sslcommerze_get(price, order)
        return Response(data={"session": session, "gateway": gateway}, status=status.HTTP_200_OK)


class SSLCommerzSuccess(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    def post(self, request, format=None):
        FRONTEND_SUCCESS_URL = config('FRONTEND_SUCCESS_URL', default="http://localhost:3000/payment/success/")
        transaction = request.POST.get("tran_id")
        order = Order.objects.filter(id=transaction).first()
        order.is_paid = True
        order.save()
        return HttpResponseRedirect(FRONTEND_SUCCESS_URL)

class SubscriberViewset(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()

class PasswordResetView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                print(user.email)
                # uid = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                email_body = 'Hello, please use this token for resetting your password  \n' + token
                data = {
                    'email': user.email,
                    'email_subject': 'Reset Your Password',
                    'email_body': email_body
                }
                send_mail(subject='Reset Your Password', message=email_body, from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=[user.email])
            return Response({'data': 'An email has been sent for resetting your password. Please check'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Please input a correct email'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)