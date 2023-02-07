from dj_rest_auth.serializers import UserDetailsSerializer, PasswordResetSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from apps.ecommerce.models import Product, Category, DiscountCategory, MainBanner, ProductImage, Order, OrderItem, \
    Advertisement, Subscriber

User = get_user_model()

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    details = serializers.ImageField(read_only=True)
    card = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ['image', 'details', 'card']


class ProductSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class DCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCategory
        fields = "__all__"


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = "__all__"


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'price']
        extra_kwargs = {
            'product': {'validators': []},
        }

    def get_product_name(self, obj):
        if obj.product is not None:
            return obj.product.name
        else:
            return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items:
            OrderItem.objects.create(order=order, **item)
            product = Product.objects.get(id=item['product'].id)
            product.stock -= item['quantity']
            if product.stock>0:
                product.save()
            else:
                raise ValidationError({"error": "Product stock out"}, code='invalid')
        return order


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = "__all__"


class MyPasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account.forms import default_token_generator
        else:
            from django.contrib.auth.tokens import default_token_generator

        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
        }

        opts.update(self.get_email_options())
        print(opts)
        self.reset_form.save(**opts)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['email', 'password', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            email = attrs.get('email')

            user = User.objects.get(email=email)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset token is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

        return super().validate(attrs)

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username','first_name', 'last_name', 'email']
        read_only_fields = ['pk']

