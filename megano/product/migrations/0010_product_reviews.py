# Generated by Django 5.0 on 2024-02-16 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_remove_specifications_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.reviews'),
            preserve_default=False,
        ),
    ]
