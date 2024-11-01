# Generated by Django 5.0 on 2024-05-07 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0023_alter_category_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('delivery_type', models.CharField(choices=[('Delivery', 'Delivery'), ('Express delivery', 'Express delivery')], max_length=50)),
                ('payment_type', models.CharField(choices=[('Online card', 'Online card'), ('Online from random someone else`s account', 'Online from random someone else`s account')], max_length=50)),
                ('totalCost', models.DecimalField(decimal_places=1, max_digits=10)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Unaccepted', 'Unaccepted')], max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('products', models.ManyToManyField(related_name='order_products', to='product.product')),
            ],
        ),
    ]
