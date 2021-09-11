from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "category"


class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ManyToManyField(Category)
    specifications = models.JSONField(null=True)

    class Meta:
        db_table = "product"


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