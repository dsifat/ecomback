# Generated by Django 3.2.6 on 2023-01-18 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0033_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ManyToManyField(to='ecommerce.Product'),
        ),
    ]