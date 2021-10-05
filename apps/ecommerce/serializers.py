from rest_framework import serializers

from apps.ecommerce.models import Product, Category, DiscountCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCategory
        fields = "__all__"
