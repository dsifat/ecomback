from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


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
    specifications = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    review = models.IntegerField(default=0)
    ratings = models.FloatField(default=0.0)
    until = models.DateField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
    sold = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0, blank=True)
    sale_percentage = models.FloatField(default=0.00)
    sale = models.BooleanField(default=False)
    sale_price = models.IntegerField(default=0)
    top = models.BooleanField(default=False)
    # discount_category = models.ManyToManyField("ecommerce.DiscountCategory", null=True, blank=True)
    validity = models.DateTimeField(null=True, blank=True)
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
    cart = models.JSONField()
    date = models.DateTimeField()
    location = models.JSONField()
    is_paid = models.BooleanField(null=True)
    payment_mode = models.JSONField(null=True)
    

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
