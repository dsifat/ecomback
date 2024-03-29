# Generated by Django 3.2.6 on 2021-09-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_auto_20210827_0310'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_category',
            field=models.ManyToManyField(to='ecommerce.DiscountCategory'),
        ),
    ]
