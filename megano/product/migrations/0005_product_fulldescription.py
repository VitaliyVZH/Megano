# Generated by Django 5.0 on 2024-02-11 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='fullDescription',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
