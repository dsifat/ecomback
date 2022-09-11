# Generated by Django 3.2.6 on 2022-09-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_auto_20220912_0214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Products'},
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ManyToManyField(blank=True, null=True, to='ecommerce.Brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_category',
            field=models.ManyToManyField(blank=True, null=True, to='ecommerce.DiscountCategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percentage',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
