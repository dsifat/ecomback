from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.ecommerce.models import Product, Category, DiscountCategory, ProductImage, MainBanner, Order, Advertisement, \
    OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image', 'image_img']
    readonly_fields = ['image_img']
    @mark_safe
    def image_img(self, obj):
        if obj.image:
            return '<img src="%s"  width="50px"/>' % obj.image.url
        else:
            return "N/A"
    image_img.allow_tags = True

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'stock', 'price']
    search_fields = ['code', 'name']
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

class OrderItemInline(admin.TabularInline):
    model = OrderItem

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'location', 'created_at', 'total', 'is_paid']
    list_filter = ['created_at']
    readonly_fields = ['location', 'payment_mode', 'order_total', 'discount', 'total', 'name', 'phone']
    list_per_page = 20
    fields = ['name', 'location', 'order_total', 'discount', 'total', 'payment_mode', 'is_paid', 'status']
    inlines = [
        OrderItemInline
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Order, OrderAdmin)

admin.site.index_template = "admin/custom_admin.html"
admin.autodiscover()
