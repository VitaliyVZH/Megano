# Generated by Django 5.0 on 2024-03-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_alter_productimage_product_alter_reviews_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='product.tag'),
        ),
    ]
