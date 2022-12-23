from django.contrib import admin

from apps.ecommerce.models import Product, Category, DiscountCategory, ProductImage, MainBanner, Order, Advertisement


class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline
    ]


admin.site.register(Product, ProductAdmin)

# class ProductImageAdmin(admin.ModelAdmin):
#     pass
#
#
# admin.site.register(ProductImage, ProductImageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


class DiscountCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(DiscountCategory, DiscountCategoryAdmin)

class MainBannerAdmin(admin.ModelAdmin):
    pass
admin.site.register(MainBanner, MainBannerAdmin)

class AdvertisementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Advertisement, AdvertisementAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)