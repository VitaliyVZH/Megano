# Generated by Django 5.0 on 2024-09-27 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_rename_created_at_order_createdat_and_more'),
        ('payment', '0002_payment_payment_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_num_orders',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='order.order'),
            preserve_default=False,
        ),
    ]