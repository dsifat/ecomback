from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Category"


class Product(models.Model):
    name = models.CharField(max_length=256)
    category = models.ManyToManyField(Category)

    class Meta:
        db_table = "Product"
