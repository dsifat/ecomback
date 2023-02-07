from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField


User = get_user_model()

# class User(AbstractUser):
#     pass

class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='category')
    thumbnail = ImageSpecField(source="image",
                             processors=[ResizeToFill(300, 300)],
                             format="JPEG")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "category"
        verbose_name_plural = "Categories"

class Brand(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ManyToManyField(Category, related_name="products")
    slug = models.SlugField(max_length=256, null=True, blank=True)
    short_description = models.TextField(max_length=512, null=True, blank=True)
    specifications = RichTextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    code = models.CharField(max_length=60, null=True, blank=True)
    # review = models.IntegerField(default=0)
    ratings = models.FloatField(default=0.0)
    # until = models.DateField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
    sold = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0, blank=True)
    # sale_percentage = models.FloatField(default=0.00)
    sale = models.BooleanField(default=False)
    sale_price = models.IntegerField(default=0, blank=True)
    top = models.BooleanField(default=False)
    # discount_category = models.ManyToManyField("ecommerce.DiscountCategory", null=True, blank=True)
    # validity = models.DateTimeField(null=True, blank=True)
    # images = models.JSONField(null=True, blank=True)
    brand = models.ManyToManyField("ecommerce.Brand", related_name="products", null=True, blank=True)

    class Meta:
        db_table = "product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to="products")
    details = ImageSpecField(source="image",
                             processors=[ResizeToFill(800,800)],
                             format="JPEG")
    card = ImageSpecField(source="image",
                          processors=[ResizeToFill(300,300)],
                          format="JPEG")
    class Meta:
        db_table = "product_image"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

class Stock(models.Model):
    product_code = models.CharField(max_length=20)
    stock = models.IntegerField(default=0)


class Order(models.Model):
    payment_status = (
        (0, 'Cash on Delivery'),
        (1, 'SSL Commerze')
    )
    status = (
        (1, 'Initiated'),
        (2, 'Completed'),
        (3, 'Cancel')
    )
    # cart = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.TextField()
    is_paid = models.BooleanField(default=False)
    payment_mode = models.IntegerField(choices=payment_status)
    order_total = models.FloatField(default=0.00)
    discount = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)
    name = models.CharField(max_length=127)
    phone = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=status, default=1)

    def __str__(self):
        return f"{id}"

    @property
    def created_date(self):
        return self.created_at.date()

    @property
    def created_time(self):
        return self.created_at.time()

# @receiver(post_save, sender=Order)
# def on_status_update(sender, instance, created, **kwargs):
#     # write you functionality
#     items = instance.items
#     print(items)
#     if created:
#         print(instance.id)
#         items = OrderItem.objects.filter(order_id=61)
#         if items.exists():
#             for item in items:
#                 product = get_object_or_404(Product, id=item.product.id)
#                 product.stock -= 1
#                 product.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f"{self.order.id}"

    @property
    def product_name(self):
        return self.product.name


class PaymentMode(models.Model):
    name = models.CharField(max_length=120)


class DiscountCategory(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

class MainBanner(models.Model):
    name = models.CharField(max_length=50)
    caption = models.CharField(max_length=127)
    image = models.ImageField(upload_to="main-banner/",null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Advertisement(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    caption = models.CharField(max_length=127, null=True, blank=True)
    image = models.ImageField(upload_to="advertisement/", null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Subscriber(models.Model):
    email = models.EmailField(max_length=30, unique=True)
    status = models.BooleanField(default=False)