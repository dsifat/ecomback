# Generated by Django 3.2.6 on 2022-10-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='ecommerce.Category'),
        ),
    ]
