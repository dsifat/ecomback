from django.contrib import admin

from apps.ecommerce.models import Product, Category, DiscountCategory


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


class DiscountCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(DiscountCategory, DiscountCategoryAdmin)
