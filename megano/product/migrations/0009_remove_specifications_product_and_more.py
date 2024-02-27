# Generated by Django 5.0 on 2024-02-16 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_product_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specifications',
            name='product',
        ),
        migrations.AddField(
            model_name='specifications',
            name='specifications',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
            preserve_default=False,
        ),
    ]
