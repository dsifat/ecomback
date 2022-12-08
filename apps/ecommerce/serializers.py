from rest_framework import serializers

from apps.ecommerce.models import Product, Category, DiscountCategory, MainBanner, ProductImage


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