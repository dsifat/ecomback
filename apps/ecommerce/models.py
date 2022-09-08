from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# class User(AbstractUser):
#     username = models.CharField(max_length=11, verbose_name='Mobile No', unique=True, validators=[
#         RegexValidator(regex='(^(01){1}[3-9]{1}\d{8})$', message='Enter a valid phone number'), ])
#     first_name = None
#     last_name = None
#     name = models.CharField(max_length=100)
#     photo = models.ImageField(null=True, blank=True)
#     mobile_no = models.CharField(max_length=11, verbose_name="Mobile No", unique=True, validators=[
#         RegexValidator(regex='(^(01){1}[3-9]{1}\d{8})$', message='Enter a valid phone number'), ], null=True,
#                                  blank=True)
#     mobile_verified = models.BooleanField(default=False)
#     email = models.EmailField(unique=True, null=True, blank=True)
#     age = models.CharField(max_length=100, null=True, blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     map_location = models.CharField(max_length=320, null=True, blank=True)
#     address = models.CharField(max_length=127, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "category"

class Brand(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=256, null=True, blank=True)
    specifications = models.JSONField(null=True)
    price = models.IntegerField(default=0)
    discount_percentage = models.IntegerField(default=0)
    discount_category = models.ManyToManyField("ecommerce.DiscountCategory")
    validity = models.DateTimeField(null=True, blank=True)
    images = models.JSONField(null=True)
    brand = models.ManyToManyField("ecommerce.Brand")

    class Meta:
        db_table = "product"

    def __str__(self):
        return f"{self.name}"

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
