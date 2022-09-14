import graphene
from graphene_django import DjangoObjectType

from apps.ecommerce.models import Product, Category


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ['id', 'name']

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_products(root, info):
        return Product.objects.all()


schema = graphene.Schema(query=Query)